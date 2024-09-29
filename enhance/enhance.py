# load packages
from openai import OpenAI

import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# load restaurant information inputs
from inputs.restaurant_info.name import name
from inputs.restaurant_info.location import location
from inputs.restaurant_info.cuisine import cuisine
from inputs.restaurant_info.nationalities import nationalities

# load given menu inputs
from inputs.menus.given_menu import given_menu

# load schemas
from enhance.schemas.given_menu_schema import given_menu_schema
from enhance.schemas.intermediate_step_schema import intermediate_step_schema
from enhance.schemas.enhanced_menu_schema import enhanced_menu_schema

# load functions
from enhance.validate import dish_exists

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
<name> {name} </name>
<location> {location} </location>
<cuisine> {cuisine} </cuisine>
<nationalities> {nationalities} </nationalities>
<menu> {given_menu} </menu>
"""

try:
     validate(instance=given_menu, schema=given_menu_schema)
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
               if not dish_exists(given_menu, menu_item['name']):  # if generated dish does not exist, regenerate content
                    valid = False
                    print(f"Generated menu item {menu_item['name']} does not exist.")
                    break
               for upsell in menu_item['recommended_upsells']:
                    if not dish_exists(given_menu, upsell):  # if generated upsell does not exist, regenerate content
                         valid = False
                         print(f"Recomended upsell {upsell} for generated menu item {menu_item['name']} does not exist.")
                         break
               print(f'Validating {menu_item['narrative']['nationality']} is in nationalities {nationalities} list...')
               if menu_item['narrative']['nationality'] not in nationalities:
                    valid = False
                    print(f"Mentioned nationality {menu_item['narrative']['nationality']} is not mentioned in guest nationalities.")
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