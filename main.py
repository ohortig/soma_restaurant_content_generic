# imports
## load packages
from openai import OpenAI
import json
import os
from enhance import enhance

## load content framework
from inputs.frameworks.content_framework import content_framework
## load restaurant info
from inputs.restaurant_info import RESTAURANT_INFO
## load response schemas
from inputs.frameworks.quiz_schema import quiz_json_schema

## to check generated content for accuracy
from review import review

## load enhanced menus
print()
print("Loading enhanced menu...")
file_path = file_path = os.path.join('outputs', 'enhanced_menus', 'consolidated_menu.json')
try:
	with open(file_path, 'r') as file:
		enhanced_menu = json.load(file)
	print("Enhanced menu loaded.")
except FileNotFoundError:
	print(f"The directory for {file_path} does not exist.")
	print("\n**************************")
	print("Creating enhanced menu...")
	print("**************************\n")
	enhance()
	with open(file_path, 'r') as file:
		enhanced_menu = json.load(file)
	print("\nEnhanced menu loaded.")

# set up enhancement

client = OpenAI()
generated_content = [None] * len(content_framework)  # list to be filled with structured content adhering to the content framework

valid = True
# setup before running

# generate quiz content for every section in content_framework.py

print("\n**************************")
print("Generating content...")
print("**************************\n")


# for section in range(len(content_framework)):  # for every section (1-5)
# changed section calling with names ("to specify it better")
for section in content_framework.keys():  #  **TESTING** for one section (1)
	print(f"Generating section {section}:")
	generated_content[section] = {"title": content_framework[section]["title"], "quizzes": []}  # add section to content
	#for quiz in range(len(content_framework[section]["quizzes"])):  # for every quiz (1-10) in the selected section
	quizzes = content_framework[section]["quizzes"]
	for quiz in quizzes.keys():  #  **TESTING** for one quizzes
		example_questions = ""
		for question in content_framework[section]["quizzes"][quiz]["example_questions"]:
			example_questions += question["example"] + "\n"
		system_message_content = """
		<instructions>
		You are a helpful assistant which develops comprehensive, scenario-based quiz modules designed to effectively train restaurant staff by enhancing their proficiency in diverse areas, including menu knowledge, cultural understanding, waiter etiquette, sales techniques, and more.
		The quizzes should be engaging, contextually relevant, and varied to ensure high levels of interest without redundancy.
		</instructions>

		<inputs>
		Use the following inputs to generate the quiz:
		### 1. **Title of Section**: The title of the section the quiz is part of.
		### 2. **Description of Section**: A high level description of the section the quiz is in.
		### 3. **Title of Quiz**: The name of the quiz that you are generating.
		### 4. **Description of Quiz**: A high level description of the quiz that you are generating.
		### 5. **Restaurant Name**: The name of the restaurant.
		### 6. **Restaurant Location**: The restaurant's location
		### 7. **Nationalities**: The top  nationalities of the restaurant's clientele.
		### 8. **Cuisine of the Restaurant**: The main cuisine featured at the restaurant.
		### 9. **Restaurant Context**: A summary of the history, aesthetic, and mission statemnent of the restaurant
		### 10. **Example Quiz Question(s)**: Examples of the sort of question you should be generating.
		### 11. **Enhanced Menus**: Enhanced menus which detail the pricing, ingredients, pairing suggestions, cultural narratives, and menu category for each menu item. 
		</inputs>

		<output_requirements>
		### 1. **Generate Questions**:
		Develop a diverse set of scenario-based questions tailored to the input data. 
		Ensure questions are engaging, diverse, framed in real-world scenarios, and not repetitive to maintain quiz freshness and intrigue. 
		### 2. **Structure of the Quiz**:
		Each quiz should contain 10 questions with multiple-choice answers (A to D), with one correct answer. In answer_explanation, explain why the chosen answer is correct.
		Follow the response_format json schema completely, with zero deviations.
		</output_requirements>
		"""
		user_message_content = f"""
		### 1. **Title of Section**: {content_framework[section]["title"]}
		### 2. **Description of Section**: {content_framework[section]["description"]}
		### 3. **Title of Quiz**: {content_framework[section]["quizzes"][quiz]["title"]}
		### 4. **Description of Quiz**: {content_framework[section]["quizzes"][quiz]["description"]}
		### 5. **Restaurant Name**: {RESTAURANT_INFO.name}
		### 6. **Restaurant Location**: {RESTAURANT_INFO.location}
		### 7. **Nationalities**: {RESTAURANT_INFO.nationalities}
		### 8. **Cuisine of the Restaurant**: {RESTAURANT_INFO.cuisine}
		### 9. **Restaurant Context**: {RESTAURANT_INFO.restaurant_context}
		### 10. **Example Quiz Questions**: {example_questions}
		### 11. **Enhanced Menus**: {enhanced_menu}
					"""
		print("\t***")
		print(f"\tGenerating quiz {quiz} in section {section}...")
		print("\t***")
		while True:
			try:  #  handle API refusals
				completion = client.chat.completions.create(
					model="gpt-4o-2024-08-06",  # fined-tuned question generation model
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
						"json_schema": quiz_json_schema
					}
				)
			except Exception as e:  # handle errors like finish_reason, refusal, content_filter, etc.  ## in case Chat Completion API is unable to follow response_format schema
				if completion.choices[0].message.refusal is not None:
					print(f"** Error ** API refused to respond. Reason: {completion.choices[0].message.refusal}")
				else:
					print(f"** Error ** {e}")
				valid = False
				break
			generated_questions = json.loads(completion.choices[0].message.content)
			new_content = {
				"title": content_framework[section]["quizzes"][quiz]["title"],
				"description": content_framework[section]["quizzes"][quiz]["description"],
				"questions": generated_questions["Quiz"]
			}
			print(f"\t<< Quiz {quiz} generated >>")
			print("\tReviewing generated content for quality and hallucination...")
			print("\t***")
			if(review(new_content, enhanced_menu, RESTAURANT_INFO.nationalities)):
				break
			else:
				print("\n\t***")
				print("\t** Error ** Regenerating quiz...")
				print("\t***\n")

		print(f"\n\t<< Quiz {quiz} in section {section} successfully generated >>\n")
		generated_content[section]["quizzes"].append(new_content)  # add new content to appropriate section in content data structure
	print(f"\n\t<< Section {section + 1} successfully generated >>\n")

file_path = os.path.join('outputs', 'generated_content.json')

if valid:  # create storage file if content is valid
	try:
		with open(file_path, 'w') as json_file:
			json.dump(generated_content, json_file, indent=4) 
			print(f"\nGenerated content stored in {file_path}.\n")
	except FileNotFoundError:
		print(f"The directory for {file_path} does not exist.")