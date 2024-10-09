import json
import os

def print_quizzes_nicely(data):
     content = ""
     if not data:
          return "No data found"
     try:
          for section in data:
               # Make sure section has a title key
               if 'title' not in section:
                    content += "\n(No title found for this section)"
               else:
                    content += f"\n{section['title']}"

               # Proceed to the quizzes if available
               quizzes = section.get('quizzes', [])
               for quiz_index, quiz in enumerate(quizzes):
                    content += f"\n  Quiz {quiz_index + 1}: {quiz.get('title', '(No title)')}"
                    content += f"\n    Description: {quiz.get('description', '(No description)')}"
                    content += "\n    Questions:"
                    questions = quiz.get('questions', {})
                    
                    # Iterate through questions if they exist
                    for q_key, question in questions.items():
                         content += f"\n      {q_key}: {question.get('question', '(No question)')}"
                         content += f"\n        A: {question.get('A', '(No option A)')}"
                         content += f"\n        B: {question.get('B', '(No option B)')}"
                         content += f"\n        C: {question.get('C', '(No option C)')}"
                         content += f"\n        D: {question.get('D', '(No option D)')}"
                         content += f"\n        Correct Answer: {question.get('correct_answer', '(No correct answer)')}"
                         content += f"\n        Explanation: {question.get('answer_explanation', '(No explanation)')}"
     except Exception as e:
          pass
          
     return content

file_path = os.path.join('outputs', 'generated_content.json')

# Try to load the file and check its content
try:
    with open(file_path, 'r') as file:
        content = json.load(file)
except FileNotFoundError:
    print(f"Error: File not found at path {file_path}")
    content = None

if content:
    result = print_quizzes_nicely(content)
    try:
          file_path = 'output.txt'
          with open(file_path, 'w') as file:
               file.write(result)
    except Exception as e:
        print(f"Error writing to file: {e}")
else:
    print("No content to process.")