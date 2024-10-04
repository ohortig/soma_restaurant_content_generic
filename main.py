# load packages
from openai import OpenAI
import json
import os

# load content framework
from inputs.frameworks.content_framework import content_framework

# load API inputs
## load enhanced menus
file_path = file_path = os.path.join('outputs', 'enhanced_menus', 'consolidated_menu.json')
try:
	with open(file_path, 'r') as file:
		enhanced_menu = json.load(file)
except FileNotFoundError:
	print(f"The directory for {file_path} does not exist.")

## load restaurant info
from inputs.restaurant_info.cuisine import cuisine
from inputs.restaurant_info.location import location
from inputs.restaurant_info.name import name
from inputs.restaurant_info.nationalities import nationalities

## load quiz response schema
from inputs.frameworks.json_schema_single_quiz import json_schema

client = OpenAI()

generated_content = [None] * len(content_framework)  # list to be filled with structured content adhering to the content framework

for section in range(len(content_framework)):  # for every section (1-5)
	generated_content[section] = []
	generated_content[section].append({"title": content_framework[section]["title"], "quizzes": []})  # add section to content
	for quiz in range(len(content_framework[section]["quizzes"])):  # for every quiz (1-10) in the selected section
		system_message_content = """
<instructions>
You are a helpful assistant which develops comprehensive, scenario-based quiz modules designed to effectively train restaurant staff by enhancing their proficiency in diverse areas, including menu knowledge, cultural understanding, waiter etiquette, sales techniques, and more.
The quizzes should be engaging, contextually relevant, and varied to ensure high levels of interest without redundancy.
</instructions>

<inputs>
Use the following inputs to generate the quiz:
### 1. **Title of Section**: The title of the section the quiz is part of.
### 2. **Title of Quiz**: The name of the quiz that you are generating.
### 3. **Description of Quiz**: A high level description of the quiz that you are generating.
### 4. **Restaurant Name**: The name of the restaurant.
### 5. **Restaurant Location**: The restaurant's location
### 6. **Nationalities**: The top three nationalities of the restaurant's clientele.
### 7. **Cuisine of the Restaurant**: The main cuisine featured at the restaurant.
### 8. **Enhanced Menus**: Enhanced menus which detail the pricing, ingredients, pairing suggestions, cultural narratives, and menu category for each menu item. 
</inputs>

<output_requirements>
### 1. **Generate Questions**:
Develop a diverse set of scenario-based questions tailored to the input data. 
Ensure questions are engaging, diverse, framed in real-world scenarios, and not repetitive to maintain quiz freshness and intrigue. 
### 2. **Structure of the Quiz**:
Each quiz should contain 10 questions with multiple-choice answers (A to D), with one correct answer.
Follow the response_format json schema completely, with zero deviations.
</output_requirements>
"""
		user_message_content = f"""
### 1. **Title of Section**: {content_framework[section]["title"]}
### 2. **Title of Quiz**: {content_framework[section]["quizzes"][quiz]["title"]}
### 3. **Description of Quiz**: {content_framework[section]["quizzes"][quiz]["description"]}
### 4. **Restaurant Name**: {name}
### 5. **Restaurant Location**: {location}
### 6. **Nationalities**: {nationalities}
### 7. **Cuisine of the Restaurant**: {cuisine}
### 8. **Enhanced Menus**: {enhanced_menu}
    		"""
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
				"questions": completion.choices[0].message.content
			}
			generated_content[section].append(new_content)  # add new content to appropriate section and quiz in content data structure
		except Exception as e:  # handle errors like finish_reason, refusal, content_filter, etc.  ## in case Chat Completion API is unable to follow response_format schema
			print(f"** Error ** API refused to respond. Reason: {completion.choices[0].message.refusal}")

file_path = os.path.join('outputs', 'generated_content.json')
try:
	with open(file_path, 'w') as json_file:
          json.dump(generated_content, json_file, indent=4) 
          print(f"Storing generated content in {file_path}.")
except FileNotFoundError:
	print(f"The directory for {file_path} does not exist.")
