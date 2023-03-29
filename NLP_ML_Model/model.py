from transformers import pipeline
bert = pipeline("question-answering", model='distilbert-base-uncased-distilled-squad')

def model_response_detailed(result):
    print(f"\nAnswer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")

def model_response(result):
    print(f"\n\n{result['answer']}")

def ask_model(asked_question: str, given_context: str):
    answer = bert(question = asked_question, context = given_context)
    return model_response(answer)


if __name__ == "__main__":
    ask_model("When is Assignment 1 due?", "Assignment 0 is due May 10, Assignment 2 is due Tomorrow, Assignment 1 is due Yesterday")