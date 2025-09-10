#https://medium.com/@anil.goyal0057/building-a-simple-rag-system-with-langchain-faiss-and-ollama-mistral-model-822b3245e576
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_community.document_loaders import WikipediaLoader

# loader = TextLoader("data/sampleText/Alice Adventures in Wonderland.txt", encoding="utf-8")  #Path to File
# documents = loader.load()
# docs = text_splitter.split_documents(documents)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def store_wikipedia_embeddings(docs, collection):
    PGVector.from_documents(
        documents=docs,
        embedding=embedding,
        embedding_length=384,
        create_extension=True,
        # collection_name="Wikipedia: " + collection,
        connection="postgresql://postgres:admin@127.0.0.1:5432/advanced_RAG",
        # collection_metadata= 
    )

def add_wikipedia_page(page: str):
    loader = WikipediaLoader(query=page, load_max_docs=1)
    documents=loader.load()
    for doc in documents:
        print("Loaded", doc.metadata["title"])
    docs = text_splitter.split_documents(documents)
    store_wikipedia_embeddings(docs, documents[0].metadata["title"])

add_wikipedia_page(input("What page to add?: "))

