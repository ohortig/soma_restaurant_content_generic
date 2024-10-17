# load packages
from openai import OpenAI
import json

# load functions
from utils import item_exists
from utils import nationality_exists

# load schema
from inputs.frameworks.validate_tools import validate_call_tools
from inputs.validation_prompts import review_prompts
# To load OPENAI keys
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def review_quiz(content, menu, nationalities):
     # system message
     system_message = review_prompts.review_quiz_system_prompt+"\n"+f"""<context>
     ** The restaurant's menu is <menu> {menu} </menu>
     ** The restaurant's top guest nationalities are <nationalities> {nationalities} </nationalities>
     </context>"""

     # formatting questions for review
     content = [k + ": " + v["question"] +"\n" for k, v in content.items()][0]
     
     completion = client.chat.completions.create(
          model="gpt-4o-mini", 
          messages=[
               {
               "role": "system", 
               "content": system_message
               },
               {
               "role": "user",
               "content": content
               }
          ],
          tools=validate_call_tools,
          tool_choice="required",
     )

     print(f"\t{content} >")

     for function_call in completion.choices[0].message.tool_calls:
          arguments = json.loads(function_call.function.arguments)
          function_name = function_call.function.name

          if function_name == "dish_exists":
               print(f'\tValidating {arguments["item_name"]} exists...')

               if not item_exists(arguments["item_name"]):
                    print(f"\t\t Mentioned menu item {arguments['item_name']} does not exist.")
                    return False  # regenerate the quiz

               print(f'\t\tMentioned item {arguments["item_name"]} confirmed to exist.')

          if function_name == "nationality_exists":
               print(f'\tValidating {arguments["nationality"]} is in nationalities list...')

               if not nationality_exists(arguments["nationality"]):
                    print(f"\t\tMentioned nationality {arguments['nationality']} is not mentioned in guest nationalities.")
                    return False  # regenerate the quiz

               print(f"\t\t{arguments['nationality']} confirmed in nationalities list.")

     print("\t***")
     return True

def review_choices(content, menu, nationalities):
     # system message
     system_message = review_prompts.review_choices_system_prompt+"\n"+f"""
<context>
** The restaurant's menu is <menu> {menu} </menu>
** The restaurant's top guest nationalities are <nationalities> {nationalities} </nationalities>
</context>
"""
     # formatting questions for review
     choice_data = [k +": "+ v +"\n" for k, v in content.items()][0]

     #  check that it does not have hallucination and is high-quality & scenario-based using API function calling
     ## check for hallucination
     completion = client.chat.completions.create(
          model="gpt-4o-mini", 
          messages=[
               {
               "role": "system", 
               "content": system_message
               },
               {
               "role": "user",
               "content": choice_data
               }
          ],
          tools=validate_call_tools,
          tool_choice="required",
     )

     #print(f"\t{choice_key} >")

     for function_call in completion.choices[0].message.tool_calls:
          arguments = json.loads(function_call.function.arguments)
          function_name = function_call.function.name
          if function_name == "dish_exists":
               print(f'\tValidating {arguments["item_name"]} exists...')
               if not item_exists(arguments["item_name"]):
                    print(f"\t\t Mentioned menu item {arguments['item_name']} does not exist.")
                    return False  # regenerate the quiz
               print(f"\t\tMentioned item {arguments['item_name']} confirmed to exist.")
          #if function_name == "nationality_exists":
          #     print(f'\tValidating {arguments["nationality"]} is in nationalities list...')
          #     if not nationality_exists(arguments["nationality"]):
          #          print(f"\t\tMentioned nationality {arguments["nationality"]} is not mentioned in guest nationalities.")
          #          return False  # regenerate the quiz
          #     print(f"\t\t{arguments["nationality"]} confirmed in nationalities list.")
     print("\t***")
     return True