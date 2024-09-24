# load packages
from openai import OpenAI
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# load restaurant information inputs
from inputs.restaurant_info.name import name
from inputs.restaurant_info.location import location
from inputs.restaurant_info.cuisine import cuisine
from inputs.restaurant_info.nationalities import nationalities

# load given menu inputs
from inputs.menus.dinner_menu import dinner_menu

# load schemas
from given_menu_schema import given_menu_schema
from intermediate_step_schema import intermediate_step_schema
from enhanced_menu_schema import enhanced_menu_schema

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
- ** Recommended Upsells **: Enrich our restaurant's menu by creating an Array of Strings for Upselling Recommendations: for each menu item, provide practical strategies for waitstaff to upsell to the customer. This could include recommending additional items, portion increases, premium ingredients, or add-ons like sauces, sides, or drink pairings from the restaurant's own menu.
- ** Narrative **: Enrich our restaurant's menu by creating a narrative String: an intricate and engaging narrative that connects each menu item with the cultural backgrounds of the three most frequent nationalities among our guests.
- ** Appeal **: Enrich our restaurant's menu by creating an appeal String: Highlight the textures and sensory experience of each menu item, emphasizing what makes them appealing on a tactile and sensory level to encourage customers to try them.
"""

user_message_content = f"""
<name> {name} </name>
<location> {location} </location>
<cuisine> {cuisine} </cuisine>
<nationalities> {nationalities} </nationalities>
<menu> {dinner_menu} </menu>
"""

try:
     validate(instance=dinner_menu, schema=given_menu_schema)
     print("Inputted menu JSON data is valid. Running enhancements...")
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
     answer = completion.choices[0].message
     print(completion)
    
except ValidationError as e:  # if inputted JSON menu does not follow the schema correctly
    print("Inputted menu JSON data is invalid.")
    print(f"Error message: {e.message}")
    print(f"Invalid data path: {'/'.join(map(str, e.path))}")
    print(f"Schema path: {'/'.join(map(str, e.schema_path))}")