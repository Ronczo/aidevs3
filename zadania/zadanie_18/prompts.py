QUESTION_PROMPT = """
Below you can find some html code from some website and 3 questions. Read the text and try to answer the questions.
If you can't find the answer, in response write "NO".
If you can find the answer, write the answer with given id as python dictionary.
For example:
If you can't find answer for any question, write: "NO".
If you can find answer for question with id 01, write: 01 as key, and answer as value.
Do not write any additional text, only the answer.

text: {text}
questions: {questions}

Write dict normally, dont use \'\'\'
"""
