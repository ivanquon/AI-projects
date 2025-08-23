from transformers import pipeline

question = "What made John throw up?"
context = "John ate an apple today and then threw up."

question_answerer = pipeline("question-answering", model="bert-qa-model/checkpoint-750")
question_answerer(question=question, context=context)