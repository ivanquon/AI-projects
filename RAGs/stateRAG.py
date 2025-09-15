#https://python.langchain.com/docs/tutorials/qa_chat_history/#stateful-management-of-chat-history

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_postgres import PGVector
from langgraph.graph import MessagesState, StateGraph
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Specify an ID for the thread
config = {"configurable": {"thread_id": "abc123"}}
memory = MemorySaver()
llm = ChatOllama(model="llama3.1:8b")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = PGVector.from_existing_index(
    embedding=embedding,
    collection_name="Wikipedia",
    connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG"
)


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


# Step 2: Execute the retrieval.
tools = ToolNode([retrieve])


# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
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
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}

# graph_builder = StateGraph(MessagesState)
# graph_builder.add_node(query_or_respond)
# graph_builder.add_node(tools)
# graph_builder.add_node(generate)
# graph_builder.set_entry_point("query_or_respond")
# graph_builder.add_conditional_edges(
#     "query_or_respond",
#     tools_condition,
#     {END: END, "tools": "tools"},
# )
# graph_builder.add_edge("tools", "generate")
# graph_builder.add_edge("generate", END)
# graph = graph_builder.compile(checkpointer=memory)


# input_message = "Who wrote it?"

# for step in graph.stream(
#     {"messages": [{"role": "user", "content": input_message}]},
#     stream_mode="values",
#     config=config
# ):
#     step["messages"][-1].pretty_print()


    
class QAPipeline:
    def __init__(
        self,
        thread_id: str = "abc123",
        pg_connection: str = "postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG",
        collection_name: str = "Wikipedia",
        llm_model: str = "llama3.1:8b",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        # Setup config
        self.thread_id=thread_id
        self.config = {"configurable": {"thread_id": thread_id}}
        self.memory = MemorySaver()

        # Language model and embedding model
        self.llm = ChatOllama(model=llm_model)
        self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)

        # Vector store connection
        self.vector_store = PGVector.from_existing_index(
            embedding=self.embedding,
            collection_name=collection_name,
            connection=pg_connection
        )

        # Define and bind the retrieve tool
        self.retrieve_tool = self._define_tool()

        # Build RAG 
        self.rag = self._build_RAG()

    def _define_tool(self):
        @tool(response_format="content_and_artifact")
        def retrieve(query: str):
            """Retrieve information related to a query."""
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

    def ask(self, input_message: str):
        """Stream responses from the QA graph."""
        for step in self.rag.stream(
            {"messages": [{"role": "user", "content": input_message}]},
            stream_mode="values",
            config=self.config
        ):
            step["messages"][-1].pretty_print()

    def getHistory(self):
        state = self.rag.get_state(self.config).values
        if state:
            for message in state["messages"]:
                if message.type in ("human", "ai") and message.content:
                    role = "User" if message.type == "human" else "Assistant"
                    print(f"{role}: {message.content}\n")
        else:
            print("Nothing here!")
    
    def deleteHistory(self):
        self.memory.delete_thread(self.thread_id)

if __name__ == "__main__":
    qa = QAPipeline()
    qa.ask("Who wrote Harry Potter?") 
    qa.getHistory()
    print("Deleting")
    qa.deleteHistory()
    qa.getHistory()
    print("New Query")
    qa.ask("Who wrote Harry Potter?") 
    qa.getHistory()