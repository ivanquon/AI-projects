from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.RAG import RAG, addWikipediaSource
import psycopg2

class Query(BaseModel):
    query: str

class Source(BaseModel):
    source: str

app = FastAPI()
rag = RAG()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to the RAG App"}

@app.get("/sources")
async def get_sources():
    try:
        conn = psycopg2.connect(dbname="advanced_RAG", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("""
                SELECT DISTINCT cmetadata -> 'source' as article_source
                FROM langchain_pg_embedding
                """)
        results = cur.fetchall()
        conn.commit()
        conn.close()
        return results if results else ["None"]
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/sources")
async def delete_sources():
    try:
        conn = psycopg2.connect(dbname="advanced_RAG", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("""
                TRUNCATE TABLE "langchain_pg_embedding" CASCADE;
                """)
        conn.commit()
        conn.close()
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/sources")
async def add_source(source: Source):
    try:
        res = addWikipediaSource(source.source)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/rag")
async def query_rag(query: Query):
    try:
        return(rag.ask(query.query).content)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/rag")
async def get_history():
    try:
        return([{"content": message.content, "type": message.type} for message in rag.get_history()])
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/rag")
async def delete_history():
    try:
        return(rag.delete_history())
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")