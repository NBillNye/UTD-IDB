from transformers import pipeline
question_answerer = pipeline("question-answering", model='distilbert-base-uncased-distilled-squad')

context = r"""
The office phone number is 972 312 2303
"""

result = question_answerer(question="What is the office phone number",     context=context)

print(
f"\nAnswer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}"
)