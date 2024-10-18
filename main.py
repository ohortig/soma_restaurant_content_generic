# load packages
from openai import OpenAI
import json
import os

# load content framework
from inputs.frameworks.content_framework import content_framework
from inputs.main_prompts import prompts

## load restaurant info
from inputs.restaurant_info import RESTAURANT_INFO

## load response schemas
from inputs.frameworks.schemas.questions_schema import questions_schema
from inputs.frameworks.schemas.choices_schema import choices_schema
from inputs.frameworks.schemas.quiz_schema import quiz_schema

from review import review_quiz, review_choices
from dotenv import load_dotenv

load_dotenv()
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

	with open(file_path, 'r') as file:
		enhanced_menu = json.load(file)
	print("\nEnhanced menu loaded.")

client = OpenAI()

generated_content = {} # to be filled with structured content adhering to the content framework

print("\n**************************")
print("Generating content...")
print("**************************\n")

valid = True

# for section in range(len(content_framework)):  # for every section (1-5)
# changed section calling with names ("to specify it better")
testing_section = "Storytelling and Upselling Techniques"
testing_quiz = "Dish Narrative"

for section in content_framework.keys():  #  **TESTING** for one section (1)
	if section == testing_section:
		print(f"Generating section {section}:")
		generated_content[section] = {"title": content_framework[section]["title"],
                                	  "quizzes": {}}  # add section to content

		quizzes = content_framework[section]["quizzes"]
		for quiz in quizzes.keys():  #  **TESTING** for one quiz
			if quiz != testing_quiz:
				continue
			print("\t***")
			print(f"\tGenerating quiz {quiz} in section {section}...")
			print("\t***")
			specific_quiz = content_framework[section]["quizzes"][quiz]
			generated_content[section]["quizzes"][specific_quiz["title"]] = {"description": specific_quiz["description"], "questions": {}}  # add quiz to section

			# Adding questions, if exist, for format
			preloaded_questions = content_framework[section]["quizzes"][quiz]["example_questions"]

			# example questions only
			example_questions = "<Examples>\n"
			for preloaded_question in preloaded_questions:
				example_questions += "**Question:** " + preloaded_question["example"] + "\n"
			example_questions += "</Examples>"

			# example questions + answers
			example_questions_answers = "<Examples>\n"
			for preloaded_question in preloaded_questions:
				example_questions_answers += "**Question:** " + preloaded_question["example"] + "\n"
				for preloaded_answer, preloaded_answer_value in preloaded_question["answers"].items():
					example_questions_answers += "\t" + preloaded_answer + ": " + preloaded_answer_value + "\n"
			example_questions_answers += "</Examples>"

		### First API CALL TO GENERATE ANSWERS
			while True:  # create & validate questions only
				completion = None  # Initialize completion to None
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
								content_framework[section]["title"],
        						content_framework[section]["description"],
        						content_framework[section]["quizzes"][quiz]["title"],
								content_framework[section]["quizzes"][quiz]["description"],
        						RESTAURANT_INFO.name,
              					RESTAURANT_INFO.location,
                   				RESTAURANT_INFO.nationalities,
								RESTAURANT_INFO.cuisine,
        						RESTAURANT_INFO.restaurant_context,
              					example_questions,
                   				enhanced_menu)
							}
						],
						response_format={
							"type": "json_schema",
							"json_schema": questions_schema
						}
					)
					api_response = completion.choices[0].message.content

				except Exception as e:  # handle errors like finish_reason, refusal, content_filter, etc.  ## in case Chat Completion API is unable to follow response_format schema
					if completion is not None and completion.choices[0].message.refusal is not None:
						print(f"** Error ** Question API refused to respond. Reason: {completion.choices[0].message.refusal}")
					else:
						print(f"** Error ** Exception occurred: {e}")
					valid = False
					break

				generated_questions_raw = json.loads(api_response)
				generated_questions = generated_questions_raw["quiz"]

				print(f"\t<< Quiz {quiz} generated >>")
				print("\tReviewing generated content for quality and hallucination...")
				print("\t***")
				if(review_quiz(generated_questions, enhanced_menu, RESTAURANT_INFO.nationalities)):
					break
				else:
					print("\n\t***")
					print("\t** Error ** Regenerating quiz...")
					print("\t***\n")

			print(f"\n\t<< Quiz questions for {quiz} in section {section} successfully generated >>\n")
			quiz_data = content_framework[section]["quizzes"][quiz]
			print('GENERATED _QUESTIONS')
			print(">>>>", generated_questions)
			#generated_questions_dict = json.loads(generated_questions)

			generated_content[section]["quizzes"][quiz_data["title"]]["questions"] = generated_questions  # add new content to appropriate section and quiz in content data structure
			print("The type of generated questions", type(generated_questions))

   		### SECOND API CALL TO GENERATE ANSWERS
			for generated_question in generated_questions.keys():
				consecutive_invalid_generations = 0  # tracker variable
				#while True:  # create & validate answer choices for generated questions
				for i in range(0, 3, 1):
					print(f"iteration {i}")
					try:
						completion = client.chat.completions.create(
							model="gpt-4o",  # base GPT-4o model
							messages=[
								{
								"role": "system", 
								"content": prompts.system_message_example_Q_A
								},
								{
								"role": "user",
								"content": prompts.user_message_answers(
            							generated_content[section]["quizzes"][quiz_data["title"]]["questions"][generated_question]["question"],
										RESTAURANT_INFO.name,
          								RESTAURANT_INFO.location,
                  						RESTAURANT_INFO.nationalities,
                        				RESTAURANT_INFO.cuisine,
										RESTAURANT_INFO.restaurant_context,
          								example_questions_answers,
                  						enhanced_menu)
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
					
					generated_choices_raw = json.loads(completion.choices[0].message.content)
					generated_choices = generated_choices_raw["choices"]

					print(f"\t<< Answer Choices for {generated_question} in Quiz {quiz} generated >>")
					print("\tReviewing generated content for quality and hallucination...")
					print("\t***")

					if(review_choices(generated_choices, enhanced_menu, RESTAURANT_INFO.nationalities)):
						consecutive_invalid_generations = 0
						break
					else:
						print("\n\t***")
						consecutive_invalid_generations += 1
						print(f"\t** There have been {consecutive_invalid_generations}/3 consecutive invalid generations")

						if consecutive_invalid_generations == 3:
							print("\t** Pass ** question has exceeded the maximum consecutive invalid generations. Moving on...")
							break

						print("\t** Error ** Regenerating answer choices...")
						print("\t***\n")

				# add answer choices to correct quiz question
				generated_content[section]["quizzes"][quiz_data["title"]]["questions"][generated_question]["answers"] = generated_choices

				print(f"\n\t<< Answer choices for {generated_question} of {quiz} in section {section} successfully generated and loaded >>\n")
			
			print(f"\n\t<< Complete quiz questions & answers for {quiz} in section {section} successfully generated >>\n")

		print(f"\n\t<< Section {section} successfully generated >>\n")

# Save generated output
file_path = os.path.join('outputs', f'generated_content_{RESTAURANT_INFO.name}.json')

if valid:  # create storage file if content is valid
	try:
		with open(file_path, 'w') as json_file:
			json.dump(generated_content, json_file, indent=4) 
			print(f"\nGenerated content stored in {file_path}.\n")
	except FileNotFoundError:
		print(f"The directory for {file_path} does not exist.")