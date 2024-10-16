# load packages
from openai import OpenAI
import json
import os
from enhance.enhance import enhance

# load content framework
from inputs.frameworks.content_framework import content_framework
from inputs.main_prompts import prompts

# load API inputs
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

## load restaurant info
from inputs.restaurant_info import RESTAURANT_INFO

## load response schemas
from inputs.frameworks.schemas.questions_schema import questions_schema
from inputs.frameworks.schemas.choices_schema import choices_schema
from inputs.frameworks.schemas.quiz_schema import quiz_schema

from review import review

client = OpenAI()

generated_content = {} # to be filled with structured content adhering to the content framework

print("\n**************************")
print("Generating content...")
print("**************************\n")

valid = True

# for section in range(len(content_framework)):  # for every section (1-5)
# changed section calling with names ("to specify it better")
testing_section = "Menu Knowledge Mastery"
testing_quiz = "Dish Descriptions"

for section in content_framework.keys():  #  **TESTING** for one section (1)
	if section == testing_section:
		print(f"Generating section {section}:")
		generated_content[section] = {"title": content_framework[section]["title"], "quizzes": {}}  # add section to content

		quizzes = content_framework[section]["quizzes"]
		for quiz in quizzes.keys():  #  **TESTING** for one quiz
			if quiz != testing_quiz:
				continue
			print("\t***")
			print(f"\tGenerating quiz {quiz} in section {section}...")
			print("\t***")

			generated_content[section]["quizzes"][content_framework[section]["quizzes"][quiz]["title"]] = {"description": content_framework[section]["quizzes"][quiz]["description"], "questions": {}}  # add quiz to section

			# Adding questions, if exist, for format
			preloaded_questions = content_framework[section]["quizzes"][quiz]["example_questions"]

			# example questions only
			example_questions = "<Examples>\n"
			for preloaded_question in preloaded_questions:
				example_questions += "**Question:**" + preloaded_question["example"] + "\n"
			example_questions += "\n</Examples>"

			# example questions + answers
			example_questions_answers = "<Examples>\n"
			for preloaded_question in preloaded_questions:
				example_questions_answers += "**Question:**" + preloaded_question["example"] + "\n"
				for preloaded_answer in preloaded_question:
					example_questions_answers += "\t" + preloaded_answer
			example_questions_answers += "\n</Examples>"


			while True:  # create & validate questions only
				try:
					completion = client.chat.completions.create(
						model="gpt-4o-2024-08-06",  # base GPT-4o model
						messages=[
							{
							"role": "system", 
							"content": prompts.system_message_example_Q
							},
							{
							"role": "user",
							"content": prompts.user_message_question(
								content_framework[section]["title"], content_framework[section]["description"], content_framework[section]["quizzes"][quiz]["title"],
								content_framework[section]["quizzes"][quiz]["description"], RESTAURANT_INFO.name, RESTAURANT_INFO.location, RESTAURANT_INFO.nationalities,
								RESTAURANT_INFO.cuisine, RESTAURANT_INFO.restaurant_context, example_questions, enhanced_menu)
							}
						],
						response_format={
							"type": "json_schema",
							"json_schema": questions_schema
						}
					)
				except Exception as e:  # handle errors like finish_reason, refusal, content_filter, etc.  ## in case Chat Completion API is unable to follow response_format schema
					if completion.choices[0].message.refusal is not None:
						print(f"** Error ** Question API refused to respond. Reason: {completion.choices[0].message.refusal}")
						
					else:
						print(f"** Error ** {e}")
					valid = False
					break

				generated_content = json.loads(completion.choices[0].message.content)
				generated_questions = generated_content["Quiz"]

				print(f"\t<< Quiz {quiz} generated >>")
				print("\tReviewing generated content for quality and hallucination...")
				print("\t***")
				if(review(generated_questions, enhanced_menu, RESTAURANT_INFO.nationalities)):
					break
				else:
					print("\n\t***")
					print(f"\t** Error ** Regenerating quiz...")
					print("\t***\n")

			print(f"\n\t<< Quiz questions for {quiz} in section {section} successfully generated >>\n")

			generated_content[section]["quizzes"][quiz]["questions"] = generated_questions  # add new content to appropriate section and quiz in content data structure

			for generated_question in generated_questions.keys():
				while True:  # create & validate answer choices for generated questions
					try:
						completion = client.chat.completions.create(
							model="gpt-4o-mini",  # base GPT-4o mini model
							messages=[
								{
								"role": "system", 
								"content": prompts.system_message_example_Q_A
								},
								{
								"role": "user",
								"content": prompts.user_message_answers(generated_question["question"], RESTAURANT_INFO.name, RESTAURANT_INFO.location,
									   RESTAURANT_INFO.nationalities, RESTAURANT_INFO.cuisine, RESTAURANT_INFO.restaurant_context,
									   example_questions_answers, enhanced_menu)
								}
							],
							response_format={
								"type": "json_schema",
								"json_schema": choices_schema
							}
						)
					except Exception as e:  # handle errors like finish_reason, refusal, content_filter, etc.  ## in case Chat Completion API is unable to follow response_format schema
						if completion.choices[0].message.refusal is not None:
							print(f"** Error ** Answer Choice API refused to respond. Reason: {completion.choices[0].message.refusal}")
							
						else:
							print(f"** Error ** {e}")
						valid = False
						break

					generated_content = json.loads(completion.choices[0].message.content)
					generated_choices = generated_content["choices"]

					print(f"\t<< Answer Choices for Quiz {quiz} generated >>")
					print("\tReviewing generated content for quality and hallucination...")
					print("\t***")
					if(review(generated_choices, enhanced_menu, RESTAURANT_INFO.nationalities)):
						break
					else:
						print("\n\t***")
						print(f"\t** Error ** Regenerating quiz...")
						print("\t***\n")

				# add answer choices to correct quiz question
				generated_content[section]["quizzes"][quiz]["questions"][generated_question]["answers"] = generated_choices

				print(f"\n\t<< Answer choices for {quiz} in section {section} successfully generated and loaded>>\n")
			
			print(f"\n\t<< Quiz questions & answers for {quiz} in section {section} successfully generated >>\n")

		print(f"\n\t<< Section {section} successfully generated >>\n")

file_path = os.path.join('outputs', 'generated_content.json')

if valid:  # create storage file if content is valid
	try:
		with open(file_path, 'w') as json_file:
			json.dump(generated_content, json_file, indent=4) 
			print(f"\nGenerated content stored in {file_path}.\n")
	except FileNotFoundError:
		print(f"The directory for {file_path} does not exist.")