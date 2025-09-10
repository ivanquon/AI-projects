#https://python.langchain.com/docs/tutorials/rag/ And a lot of other docs
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_postgres import PGVector
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent


llm = ChatOllama(model="llama3.1:8b")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
query = input("What would you like to ask?: ")

# 
# db = SQLDatabase.from_uri("postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG")
# agent_executor = create_sql_agent(llm, db=db, verbose=True)
# collection = agent_executor.invoke(
#     f"Check the table langchain_pg_collection for collections most relevant to this query: {query}. Return only the name of the most relevant collection and nothing else"
# )["output"]

#Retrieves existing embeddings from database
vector_store = PGVector.from_existing_index(
    embedding=embedding,
    # collection_name=collection, #Default collection_name is langchain
    connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG"
)

# filters = {"source": {"$ilike": "%Alice%"}}
# retriever = vector_store.as_retriever(search_kwargs={"k": 3, "filter": filters})

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

#Template for LLM
prompt = ChatPromptTemplate.from_template(
    """Use the following context to answer the question. Tell if your answer is created from the context, if not give the source.
    
    Context:
    {context}

    Question: {question}
    Answer:"""
)

# RAG chain using LCEL
rag_chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | llm
)

result = rag_chain.invoke(query)

print("Answer:", result.content)

def askRAG(llm: ChatOllama, embedding: HuggingFaceEmbeddings, query: str):
    retriever = PGVector.from_existing_index(
        embedding=embedding,
        # collection_name=collection, #Default collection_name is langchain
        connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG"
    ).as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template(
    """Use the following context to answer the question. Tell if your answer is created from the context, if not give the source.
    
    Context:
    {context}

    Question: {question}
    Answer:"""
)
    rag_chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | llm
    )

    return rag_chain.invoke(query)