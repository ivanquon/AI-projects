#https://medium.com/@anil.goyal0057/building-a-simple-rag-system-with-langchain-faiss-and-ollama-mistral-model-822b3245e576
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

loader = TextLoader("data/sampleText/Alice Adventures in Wonderland.txt", encoding="utf-8")  #Path to File
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

store = PGVector.from_documents(
    documents=docs,
    embedding=embedding,
    collection_name="Alice In Wonderland",
    connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG"
)