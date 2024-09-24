# load packages
from openai import OpenAI
import json

# load content framework
from inputs.frameworks.content_framework import content_framework

# load API inputs
## load enhanced menus
from outputs.enhanced_menus.enhanced_dinner_menu import enhanced_dinner_menu
from outputs.enhanced_menus.enhanced_wine_list import enhanced_wine_list

## load restaurant info
from inputs.restaurant_info.cuisine import cuisine
from inputs.restaurant_info.location import location
from inputs.restaurant_info.name import name
from inputs.restaurant_info.nationalities import nationalities

## load quiz response schema
from inputs.frameworks.json_schema_single_quiz import json_schema

client = OpenAI()

generated_content = []  # list to be filled with structured content adhering to the content framework

for section in range(len(content_framework)):  # for every section (1-5)
  generated_content.append({"title": content_framework[section]["title"], "quizzes": []})  # add section to content

  for quiz in range(len(content_framework[section]["quizzes"])):  # for every quiz (1-10) in the selected section

    system_message_content = "Develop comprehensive, scenario-based quiz modules designed to effectively train restaurant staff by enhancing their proficiency in diverse areas, including menu knowledge, cultural understanding, waiter etiquette, and more. The quizzes should be engaging, contextually relevant, and varied to ensure high levels of interest without redundancy. ### 1. Collect Input Data. Acquire detailed menus, including all food items with ingredients, preparation techniques, allergen information, and pairing suggestions. 2. **Location and Main Nationality of Clients**: Gather data on the restaurant's location and the predominant nationalities of its clientele. 3. **Cuisine of the Restaurant**: Determine the main cuisine featured at the restaurant. ### 2. Generate Question Pool - Develop a diverse set of questions tagged by specific subtopics tailored to the collected data. - Ensure questions are engaging, framed in real-world scenarios, and not repetitive to maintain quiz freshness and intrigue. - Use a mix of question lengths, including short, scenario-based questions. ### 3. Structure the Quiz - Each quiz module should contain 10 questions with multiple-choice answers (A to D), with one correct answer. - Each module should have an entertaining and engaging title."
    user_message_content = f"The restaurant is called {name}. It is located in {location}. The most common client nationalities are {nationalities}. The cuisine is {cuisine}. The menus are: <menu1> {enhanced_dinner_menu} </menu1>, <menu2> {enhanced_wine_list} </menu2>. Create a quiz titled {content_framework[section]["quizzes"][quiz]["title"]} as part of a section titled {content_framework[section]["title"]}. The quiz description is as follows: {content_framework[section]["quizzes"][quiz]["description"]}."
    
    try:  # handle edge cases
      completion = client.chat.completions.create(
        model="ft:gpt-4o-2024-08-06:personal:soma-finetuned:A6uJ6VVR",  # fined-tuned model
        messages=[
          {
            "role": "system", 
            "content": system_message_content
          },
          {
            "role": "user",
            "content": user_message_content
          }
        ],
        response_format={
          "type": "json_schema",
          "json_schema": json_schema
        }
      )
      new_content = {
        "title": content_framework[section]["quizzes"][quiz]["title"],
        "description": content_framework[section]["quizzes"][quiz]["description"],
        "questions": completion.choices[0]
      }
      generated_content[section]["quizzes"].append[new_content]  # add new content to appropriate section and quiz in content data structure
    except Exception as e:  # handle errors like finish_reason, refusal, content_filter, etc.  ## in case Chat Completion API is unable to follow response_format schema
      if(completion.choices[0].message.refusal):  # if API refuses to respond
        print(f"** Error ** API refused to respond. Reason: {completion.choices[0].message.refusal}")
      pass