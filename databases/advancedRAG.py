from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_postgres import PGVector
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOllama(model="llama3:8b")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = PGVector.from_existing_index(
    embedding=embedding,
    collection_name="Alice In Wonderland",
    connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template(
    """Use the following context to answer the question.
    
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


# Step 4: Ask a question
query = "Why did Alice not like staying close to the Duchess?"
result = rag_chain.invoke(query)
print("Answer:", result)
