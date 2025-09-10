import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

new_sentence = "I ate in the United States." #Change this to query
new_embedding = model.encode(new_sentence).tolist()

conn = psycopg2.connect(dbname="RAG", user="postgres", password="admin", host="localhost")
cur = conn.cursor()

cur.execute("""
            SELECT id, content
            FROM items
            ORDER BY embedding <-> %s::vector
            LIMIT 5
            """, (new_embedding,))

results = cur.fetchall()
for row in results:
    print(row)