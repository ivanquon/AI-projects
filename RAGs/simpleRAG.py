#https://medium.com/@anil.goyal0057/building-a-simple-rag-system-with-langchain-faiss-and-ollama-mistral-model-822b3245e576
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings

model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatOllama(model="llama3.1:8b")

# Step 1: Load and chunk your data
loader = TextLoader("data/sampleText/Alice Adventures in Wonderland.txt", encoding="utf-8")  #Path to File
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Step 2: Convert chunks into embeddings and store in FAISS
vectordb = FAISS.from_documents(docs, model)

# (Optional) Save and load later
# vectordb.save_local("faiss_index")

# Step 3: Create RetrievalQA chain (RAG)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Prompt template (customize if needed)
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
