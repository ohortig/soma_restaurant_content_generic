class prompts:
	system_message_example_Q = """
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
### 6. **Restaurant Location**: The restaurant's location.
### 7. **Nationalities**: The top  nationalities of the restaurant's clientele.
### 8. **Cuisine of the Restaurant**: The main cuisine featured at the restaurant.
### 9. **Restaurant Context**: A summary of the history, aesthetic, and mission statemnent of the restaurant.
### 10. **Example Quiz Question(s)**: Examples of the sort of question you should be generating.
### 11. **Enhanced Menus**: Enhanced menus which detail the pricing, ingredients, pairing suggestions, cultural narratives, and menu category for each menu item. 
</inputs>

<output_requirements>
### 1. **Generate Questions**:
Develop a diverse set of scenario-based questions tailored to the input data. 
Ensure questions are engaging, diverse, framed in real-world scenarios, and not repetitive to maintain quiz freshness and intrigue. 
### 2. **Structure of the Quiz**:
Each quiz should contain 10 questions. Create only the questions, with no answer choices.
Follow the response_format json schema completely, with zero deviations.
</output_requirements>
	"""
    
	def user_message_question(section_title, section_description, quiz_title, quiz_description, name, location, nationalities, cuisine, context, example_Q, enhanced_menu):
		user_message_question = f"""
### 1. **Title of Section**: {section_title}
### 2. **Description of Section**: {section_description}
### 3. **Title of Quiz**: {quiz_title}
### 4. **Description of Quiz**: {quiz_description}
### 5. **Restaurant Name**: {name}
### 6. **Restaurant Location**: {location}
### 7. **Nationalities**: {nationalities}
### 8. **Cuisine of the Restaurant**: {cuisine}
### 9. **Restaurant Context**: {context}
### 10. **Example Quiz Questions**: {example_Q}
### 11. **Enhanced Menus**: {enhanced_menu}
"""
		return user_message_question
	
	system_message_example_Q_A = """
<instructions>
You are a helpful assistant which develops comprehensive, scenario-based quiz modules designed to effectively train restaurant staff by enhancing their proficiency in diverse areas, including menu knowledge, cultural understanding, waiter etiquette, sales techniques, and more.
The quizzes should be engaging, contextually relevant, and varied to ensure high levels of interest without redundancy.
</instructions>

<inputs>
Use the following inputs to generate the answer choices and the explanation for why the correct answer choice is correct for a given quiz question:
### 1. **Question**: The question you are creating answer choices for.
### 2. **Restaurant Name**: The name of the restaurant.
### 3. **Restaurant Location**: The restaurant's location.
### 4. **Nationalities**: The top  nationalities of the restaurant's clientele.
### 5. **Cuisine of the Restaurant**: The main cuisine featured at the restaurant.
### 6. **Restaurant Context**: A summary of the history, aesthetic, and mission statemnent of the restaurant.
### 7. **Example Quiz Questions**: Examples of the sort of answer choices you should be generating.
### 8. **Enhanced Menus**: Enhanced menus which detail the pricing, ingredients, pairing suggestions, cultural narratives, and menu category for each menu item. 
</inputs>

<output_requirements>
### 1. **Generate Answer Choices**:
Develop a diverse set of interesting, thoughtful answer choices to the given question and input data.
The answer choices should be in the range of 100 characters to 150 characters in length, otherwise they are considered wrong.
The correct answer choice should NOT be obvious. Instead, the answer choices should all be of similar length and make the user really think to figure out which is truly the correct answer.
Designate the correct answer choice and give a brief explanation as to why.
### 2. **Structure of the Quiz**:
Each question has multiple-choice answers A, B, C, and D, with one correct answer. In explanation, explain why the chosen answer is correct.
Follow the response_format json schema completely, with zero deviations.
</output_requirements>
"""
	
	def user_message_answers(question, name, location, nationalities, cuisine, context, example_Q_A, enhanced_menu):
		user_message_answers = f"""
### 1. **Generated Question**: {question}
### 2. **Restaurant Name**: {name}
### 3. **Restaurant Location**: {location}
### 4. **Nationalities**: {nationalities}
### 5. **Cuisine of the Restaurant**: {cuisine}
### 6. **Restaurant Context**: {context}
### 7. **Example Quiz Questions**: {example_Q_A}
### 8. **Enhanced Menus**: {enhanced_menu}
"""
		return user_message_answers
