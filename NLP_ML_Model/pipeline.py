from transformers import pipeline

class Pipeline:
    def __init__(self):
        self.question_answerer = pipeline("question-answering", model='distilbert-base-uncased-distilled-squad')
    def get_answer(self, question: str, context: str) -> str:
        result = self.question_answerer(question=question, context=context)
        print(f"\nAnswer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
        return result
    
if __name__ == '__main__':
    pipeline = Pipeline()
    context = r"""
    A portion of the grade for this course is directly tied to your participation in this class. It also includes engaging in group or other activities during class that solicit your feedback on homework assignments, readings, or materials covered in the lectures (and/or labs).

    Grading
    Criteria Exam 1: 15%, Exam 2: 15%, Programming Projects (3): 40%, Assignments (weekly): 30%
    All programming projects/exercises must be implemented only in C. Students may be asked to demonstrate their projects to the TA to receive a grade on them.
    Table below is indicative letter grade for total points scored. There may be some curving, but not guaranteed.
    """
    
    question = "What is all of the grading criteria?"
    pipeline.get_answer(question, context)