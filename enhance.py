# load packages
from openai import OpenAI

import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# load restaurant information inputs
from inputs.restaurant_info import RESTAURANT_INFO

# load schemas
from inputs.frameworks.given_menu_schema import given_menu_schema
from inputs.frameworks.intermediate_step_schema import intermediate_step_schema
from inputs.frameworks.enhanced_menu_schema import enhanced_menu_schema

# load functions
from validate import item_exists
from validate import nationality_exists

client = OpenAI()

system_message_content = """
You are a helpful assistant designed to enhance restaurant menus.

You will receive prompts with, and only with, the following input information:
- ** Restaurant's Name **: a String of the name of the restaurant you are helping.
- ** Restaurant's Location **: a JSON object including the neighborhood, city, state, and country of the restaurant you are helping. 
- ** Restaurant's Cuisine **: a String of the chosen cuisine of the restaurant you are helping.
- ** Restaurant's Top Three Guest Nationalities **: an array of Strings of the top three nationalities which visit the restaurant you are helping.
- ** Restaurant's Menu(s) **: a JSON object including the category, name, ingredients, and price of all items offered at the restaurant.

Your response, an enhanced version of every single menu item in the given menu, should strictly be in the format of a valid JSON object.

Generate an enhanced version of every single menu item in the given menu with the following information:
- ** Name **: The name of the menu item you are enriching.
- ** Recommended Upsells **: Enrich our restaurant's menu by creating an Array of Strings for Upselling Recommendations: each string must be only the name of another menu item to upsell and **must not contain any descriptions or sentences**.
- ** Narrative **: Enrich our restaurant's menu by creating a narrative String: an intricate and engaging narrative that connects each menu item with the cultural backgrounds of the three most frequent nationalities among our guests.
- ** Appeal **: Enrich our restaurant's menu by creating an appeal String: Highlight the textures and sensory experience of each menu item, emphasizing what makes them appealing on a tactile and sensory level to encourage customers to try them.
"""

user_message_content = f"""
<name> {RESTAURANT_INFO.name} </name>
<location> {RESTAURANT_INFO.location} </location>
<cuisine> {RESTAURANT_INFO.cuisine} </cuisine>
<nationalities> {RESTAURANT_INFO.nationalities} </nationalities>
<menu> {RESTAURANT_INFO.dinner_menu} </menu>
"""

def enhance():
     try:
          validate(instance=RESTAURANT_INFO.dinner_menu, schema=given_menu_schema)
          print("JSON Schema validated. Input JSON data fits requirements.")
          while True:
               print("Running enhancements...\n")
               completion = client.chat.completions.create(
                    model="gpt-4o-2024-08-06",  # model supporting structured outputs
                    messages=[{
                         "role": "system", 
                         "content": system_message_content
                    },
                    {
                    "role": "user",
                    "content": user_message_content
                    }],
                    response_format={
                         "type": "json_schema",
                         "json_schema": intermediate_step_schema
                    }
               )
               intermediate_step = completion.choices[0].message.content
               intermediate_step_data = json.loads(intermediate_step)  # turn the returned String into a JSON object
               valid = True  # checker variable as we ensure generated content is valid
               file_path = os.path.join('outputs', 'enhanced_menus', 'intermediate_step_output.json')
               os.makedirs(os.path.dirname(file_path), exist_ok=True)  # ensure the file path exists
               try:
                    with open(file_path, 'w') as json_file:
                         json.dump(intermediate_step_data, json_file, indent=4)  # write the output to JSON file in the outputs/enhanced_menus folder
                         print(f"Intermediate step generated. Recommended Upsells, Narratives, and Appeals created.\nGenerated content stored in {file_path}.\nEnsuring accuracy of information...\n")
               except FileNotFoundError:
                    print(f"The directory for {file_path} does not exist.")
                    valid = False
                    break

               for menu_item in intermediate_step_data['menu_items']:
                    if valid == False:  # if this generated menu has already been deemed invalid, break the loop and regenerate
                         break
                    print(f'Validating {menu_item['name']} exists...')
                    if not item_exists(menu_item['name']):  # if generated dish does not exist, regenerate content
                         valid = False
                         print(f"\tGenerated menu item {menu_item['name']} does not exist.")
                         break
                    print(f'\tGenerated item {menu_item['name']} confirmed to exist.')
                    for upsell in menu_item['recommended_upsells']:
                         print(f'Validating {upsell} exists...')
                         if not item_exists(upsell):  # if generated upsell does not exist, regenerate content
                              valid = False
                              print(f"\tRecomended upsell {upsell} for generated menu item {menu_item['name']} does not exist.")
                              break
                         print(f'\tGenerated item {upsell} confirmed to exist.')
                    print(f'Validating {menu_item['narrative']['nationality']} is in nationalities list...')
                    if not nationality_exists(menu_item['narrative']['nationality']):
                         valid = False
                         print(f"\tGenerated nationality {menu_item['narrative']['nationality']} is not mentioned in guest nationalities.")
                         break
                    print(f"\t{menu_item['narrative']['nationality']} confirmed in nationalities list.")
               if valid:
                    break
               else:
                    print("Generated enhancements are invalid. Trying again...")
     
     except ValidationError as e:  # if inputted JSON menu does not follow the schema correctly
          print("Inputted menu JSON data is invalid.")
          print(f"Error message: {e.message}")
          print(f"Invalid data path: {'/'.join(map(str, e.path))}")
          print(f"Schema path: {'/'.join(map(str, e.schema_path))}")

     if valid:
          print("\nGenerated enhancements validated. Consolidating enhanced menu...")
          for item in intermediate_step_data['menu_items']:
               item['category'] = next((given_item['category'] for given_item in RESTAURANT_INFO.dinner_menu if given_item['name'] == item['name']), None)
               item['ingredients'] = next((given_item['ingredients'] for given_item in RESTAURANT_INFO.dinner_menu if given_item['name'] == item['name']), None)
               item['price'] = next((given_item['price'] for given_item in RESTAURANT_INFO.dinner_menu if given_item['name'] == item['name']), None)
          file_path = os.path.join('outputs', 'enhanced_menus', 'consolidated_menu.json')
          try:
               try:
                    validate(instance=intermediate_step_data['menu_items'], schema=enhanced_menu_schema)
                    print("JSON Schema validated. Consolidated enhanced menu object fits requirements.")
                    with open(file_path, 'w') as json_file:
                         json.dump(intermediate_step_data['menu_items'], json_file, indent=4)  # write the consolidated enhanced menu to JSON file in the outputs/enhanced_menus folder
                         print(f"Storing consolidated enhanced menu in {file_path}.")
                    print(f"\nDeleting intermediate files...")
                    file_path = os.path.join('outputs', 'enhanced_menus', 'intermediate_step_output.json')
                    try:
                         os.remove(file_path)
                         print(f"{file_path} has been deleted successfully.")
                    except FileNotFoundError:
                         print(f"{file_path} does not exist.")
                    except PermissionError:
                         print(f"Permission denied: unable to delete {file_path}.")
                    except Exception as e:
                         print(f"Error: {e}")
               except ValidationError as e:
                    print("The consolidated enhanced menu object does not fit the requirements and was not stored. Check input for errors and try again.")
                    print(f"Error message: {e.message}")
                    print(f"Invalid data path: {'/'.join(map(str, e.path))}")
                    print(f"Schema path: {'/'.join(map(str, e.schema_path))}")  
          except FileNotFoundError:
               print(f"The directory for {file_path} does not exist.")
               valid = False