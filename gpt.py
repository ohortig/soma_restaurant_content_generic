# load packages
from openai import OpenAI
import json

# load content framework
from content_framework import content_framework

# load API inputs
## load enhanced menus
from inputs.enhanced_menus.enhanced_dinner_menu import enhanced_dinner_menu
from inputs.enhanced_menus.enhanced_lunch_menu import enhanced_lunch_menu
## load restaurant info
from inputs.restaurant_info.cuisine import cuisine
from inputs.restaurant_info.location import location
from inputs.restaurant_info.name import name
from inputs.restaurant_info.nationalities import nationalities
## load quiz response schema
from json_schema_single_quiz import json_schema

client = OpenAI()

for section in range(len(content_framework)):  # for every section (1-5)
  for quizzes in range(len(content_framework[section]["quizzes"])): # for every quiz (1-10) in the selected section
    completion = client.chat.completions.create(
      model="ft:gpt-4o-2024-08-06:personal:soma-finetuned:A6uJ6VVR",  # fined-tuned model
      messages=[
        {
          "role": "system", 
          "content": "Develop comprehensive, scenario-based quiz modules designed to effectively train restaurant staff by enhancing their proficiency in diverse areas, including menu knowledge, cultural understanding, waiter etiquette, and more. The quizzes should be engaging, contextually relevant, and varied to ensure high levels of interest without redundancy. ### 1. Collect Input Data. Acquire detailed menus, including all food items with ingredients, preparation techniques, allergen information, and pairing suggestions. 2. **Location and Main Nationality of Clients**: Gather data on the restaurant's location and the predominant nationalities of its clientele. 3. **Cuisine of the Restaurant**: Determine the main cuisine featured at the restaurant. ### 2. Generate Question Pool - Develop a diverse set of questions tagged by specific subtopics tailored to the collected data. - Ensure questions are engaging, framed in real-world scenarios, and not repetitive to maintain quiz freshness and intrigue. - Use a mix of question lengths, including short, scenario-based questions. ### 3. Structure the Quiz - Each quiz module should contain 10 questions with multiple-choice answers (A to D), with one correct answer. - Each module should have an entertaining and engaging title."
        },
        {
          "role": "user",
          "content": f"The restaurant is called {name}. It is located in {location}. The most common client nationalities are {client_nationality}. The cuisine is {cuisine}. The menu is {enhanced_drinks} {enhanced_lunch} {enhanced_dinner} {enhanced_wines}."
        }
      ],
      response_format={
            "type": "json_schema",
            "json_schema": json_schema
      }
    )

response_content = completion.choices[0]
parsed_content = json.loads(response_content.message.content)

# Print raw JSON
print("Raw JSON:")
print(parsed_content)

# Print formatted content
print("\nFormatted Content:")
for cycle, quizzes in parsed_content.items():
    print(f"\n{cycle}")
    for quiz in quizzes:
        for quiz_name, questions in quiz.items():
            print(f"  {quiz_name}")
            for i, (question_key, question_data) in enumerate(questions.items(), 1):
                print(f"    Question {i}:")
                print(f"      {list(question_data.keys())[0]}: {list(question_data.values())[0]}")
                for option in ['A', 'B', 'C', 'D']:
                    print(f"      {option}: {question_data[option]}")
                print(f"      Correct Answer: {question_data['correct_answer']}")
                print()