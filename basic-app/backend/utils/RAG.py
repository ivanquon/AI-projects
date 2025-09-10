from fastapi import HTTPException
from langchain_ollama import ChatOllama
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres import PGVector
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from time import time

llm = ChatOllama(model="llama3.1:8b")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
retriever = PGVector.from_existing_index(
    embedding=embedding,
    collection_name="Wikipedia",
    connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG"
).as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template(
    """Use the following context to answer the question. If you cannot derive an answer from the context, simply say "I don't know".
    
    Context:
    {context}

    Question: {question}
    Answer:"""
)

def askRAG(query: str):
    rag_chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | llm
    )

    start = time()
    result = rag_chain.invoke(query)
    end = time()
    print(f"Total time: {end - start:.2f} seconds")
    return result

def addWikipediaSource(page: str):
    loader = WikipediaLoader(query=page, load_max_docs=1)
    documents=loader.load()
    
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