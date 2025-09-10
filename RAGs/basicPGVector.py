import os
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = ["It's raining heavily outside.",
        "The weather is very stormy today.",
        "There's a strong chance of thunderstorms later.",
        "Heavy rain is expected throughout the afternoon.",
        "I had pasta for dinner last night.",
        "She cooked a delicious Italian meal.",
        "We went out for some spaghetti and wine.",
        "Dinner was a big bowl of creamy carbonara.",
        "They're planning a trip to Japan next spring.",
        "I've always wanted to visit Kyoto and Tokyo.",
        "She dreams of seeing the Eiffel Tower one day.",
        "They booked a wine tour in the south of France.",
        "We're going on a road trip across the United States.",
        "They visited the Grand Canyon during summer vacation.",
        ]

conn = psycopg2.connect(dbname="RAG", user="postgres", password="admin", host="localhost")
cur = conn.cursor()

for sentence in sentences:
    print("Embedding " + sentence)
    embedding = model.encode(sentence).tolist()
    cur.execute("INSERT INTO items (content, embedding) VALUES (%s, %s)", (sentence, embedding))

conn.commit()
cur.close()
conn.close()