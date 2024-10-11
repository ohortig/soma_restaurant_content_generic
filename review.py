# load packages
from openai import OpenAI
import json

# load functions
from utils import item_exists
from utils import nationality_exists

# load schema
from inputs.frameworks.tools_schema_validate_call import validate_call_tools

client = OpenAI()

def review(content, menu, nationalities):
     # system message
     system_message = f"""
You are a helpful assistant which helps call two functions to prevent hallucination in generative AI created restaurant quiz questions. The two functions are item_exists, which makes sure an item mentioned in the question actually appears in the restaurant's menu, and nationality_exists, which makes sure a nationality mentioned in the question is actually one of the three top nationalities to visit the restaurant.
<input>
You will be given a quiz question JSON object including the question string itself, option choices A, B, C, and D, as well as a key defining which answer is correct.
You will parse through the ENTIRE question string and ALL of the possible answer choices looking for any reference of a menu item or a nationality.
</input>
<output>
Using the provided tools, you will output function arguments to be used for either item_exists and/or nationalities exist.
## 1. **item_exists Calls**: Every time you come across a mention of a menu item, whether it be food, a wine, or any other type of item which may be on a restaurant menu, you create arguments for an item_exists funciton call to make sure it actually exists in the restaurant's menu. Do not create function calls for basic ingredients, but only for an entire dish, meal, or drink.
## 2. **nationality_exists Calls**: Every time you come across a mention of a **nationality** (a **country name**, not a state or a city), you create arguments for a nationality_exists function call to make sure it is one of the most common countries of origin to dine at the restaurant. DO NOT choose a city, state, or region.
## 3. **No Calls Needed**: If you encounter no mentions of a potential menu item or a nationality in the question or its answer choices, do not create any arguments for any function.
</output>
<context>
** The restaurant's menu is <menu> {menu} </menu>
** The restaurant's top guest nationalities are <nationalities> {nationalities} </nationalities>
</context>
"""
     questions = content["questions"]
     question_keys = questions.keys()
     for question_key in question_keys:  # iterate over every question in the generated quiz
          question_data = questions[question_key]
          #  check that it does not have hallucination and is high-quality & scenario-based using API function calling
          ## check for hallucination
          completion = client.chat.completions.create(
               model="gpt-4o-mini",  # to-do: fined-tuned model for dish_exists, nationality_exists function calls
               messages=[
                    {
                    "role": "system", 
                    "content": f"{system_message}"
                    },
                    {
                    "role": "user",
                    "content": f"{question_data}"
                    }
               ],
               tools=validate_call_tools,
               tool_choice="required",
          )
          print(f"\t{question_key} >")
          for function_call in completion.choices[0].message.tool_calls:
               arguments = json.loads(function_call.function.arguments)
               function_name = function_call.function.name
               if function_name == "dish_exists":
                    print(f'\tValidating {arguments["item_name"]} exists...')
                    if not item_exists(arguments["item_name"]):
                         print(f"\t\t Mentioned menu item {arguments["item_name"]} does not exist.")
                         return False  # regenerate the quiz
                    print(f'\t\tMentioned item {arguments["item_name"]} confirmed to exist.')
               if function_name == "nationality_exists":
                    print(f'\tValidating {arguments["nationality"]} is in nationalities list...')
                    if not nationality_exists(arguments["nationality"]):
                         print(f"\t\tMentioned nationality {arguments["nationality"]} is not mentioned in guest nationalities.")
                         return False  # regenerate the quiz
                    print(f"\t\t{arguments["nationality"]} confirmed in nationalities list.")
          print("\t***")
     
     return True