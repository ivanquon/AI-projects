from fastapi import HTTPException
from langchain_ollama import ChatOllama
from langchain_postgres import PGVector
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import MessagesState, StateGraph
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

class RAG:
    """
    Referenced: https://python.langchain.com/docs/tutorials/qa_chat_history/#stateful-management-of-chat-history
    LangChain based RAG system that answers user queries using retrieved context from a PostgreSQL database
    Implementation Notes:
        - Stores memory/history based on threads, can make more instances with unique histories by passing in different thread ids
        - Currently only searches through a single collection which stores all relevant embeddings
            - Default is Wikipedia articles
            - TODO: Add functionality to first search for the most relevant collection then pass and search within that collection in order to avoid massive collections
        - Uses Sentence-Transformers from Hugging-Face for text embeddings
        - Uses locally hosted ChatOllama models as they are free and I am broke
    """
    def __init__(
        self,
        thread_id: str = "abc123",
        pg_connection: str = "postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG",
        collection_name: str = "Wikipedia",
        llm: str = "llama3.1:8b",
        embedding: str = "all-MiniLM-L6-v2",
    ):
        #Stateful memory management related
        self.thread_id=thread_id
        self.config = {"configurable": {"thread_id": thread_id}}
        self.memory = MemorySaver()
        
        #Basic Langchain RAG requirements
        self.llm = ChatOllama(model=llm)
        self.embedding = HuggingFaceEmbeddings(model_name=embedding)
        self.vector_store = PGVector.from_existing_index(
            embedding=self.embedding,
            collection_name=collection_name,
            connection=pg_connection
        )

        #RAG Graph setup
        self.retrieve_tool = self._define_tool()
        self.rag = self._build_RAG()

    def _define_tool(self):
        @tool(response_format="content_and_artifact")
        def retrieve(query: str):
            """Retrieve information related to a query from PostgresSQL database"""
            retrieved_docs = self.vector_store.similarity_search(query, k=2)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata['source']}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs

        return retrieve

    def _query_or_respond(self, state: MessagesState):
        """Generate tool call for retrieval or respond."""
        llm_with_tools = self.llm.bind_tools([self.retrieve_tool])
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def _generate(self, state: MessagesState):
        """Generate answer."""
        recent_tool_messages = [
            message for message in reversed(state["messages"])
            if message.type == "tool"
        ][::-1]

        docs_content = "\n\n".join(doc.content for doc in recent_tool_messages)
        system_message_content = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            f"{docs_content}"
        )

        conversation_messages = [
            msg for msg in state["messages"]
            if msg.type in ("human", "system") or (msg.type == "ai" and not msg.tool_calls)
        ]
        prompt = [SystemMessage(system_message_content)] + conversation_messages
        response = self.llm.invoke(prompt)
        return {"messages": [response]}

    def _build_RAG(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("query_or_respond", self._query_or_respond)
        graph_builder.add_node("tools", ToolNode([self.retrieve_tool]))
        graph_builder.add_node("generate", self._generate)

        graph_builder.set_entry_point("query_or_respond")
        graph_builder.add_conditional_edges(
            "query_or_respond",
            tools_condition,
            {END: END, "tools": "tools"},
        )
        graph_builder.add_edge("tools", "generate")
        graph_builder.add_edge("generate", END)

        return graph_builder.compile(checkpointer=self.memory)

    def stream(self, input_message: str):
        """Stream responses from the RAG graph."""
        for step in self.rag.stream(
            {"messages": [{"role": "human", "content": input_message}]},
            stream_mode="values",
            config=self.config
        ):
            step["messages"][-1].pretty_print()

    def ask(self, input_message: str):
        """Pass the input into the RAG graph and return the last message of the final state"""
        return self.rag.invoke({"messages": [{"role": "human", "content": input_message}]}, config=self.config)["messages"][-1]

    def get_history(self):
        """Get chat history stored in state"""
        state = self.rag.get_state(self.config).values
        if state:
            messages = []
            for message in state["messages"]:
                if message.type in ("human", "ai") and message.content:
                    messages.append(message)
            return messages
        else:
            return []
    
    def delete_history(self):
        """Reset history in thread"""
        self.memory.delete_thread(self.thread_id)

def addWikipediaSource(page: str):
    loader = WikipediaLoader(query=page, load_max_docs=1)
    documents=loader.load()
    text_splitter=RecursiveCharacterTextSplitter()
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    for doc in documents:
        print("Loaded", doc.metadata["title"])
    
    if not documents:
        raise HTTPException(status_code=404, detail="Article not found")
    
    docs = text_splitter.split_documents(documents)
    
    PGVector.from_documents(
        documents=docs,
        embedding=embedding,
        collection_name="Wikipedia",
        embedding_length=384,
        create_extension=True,
        connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG",
    )
