import json
from inputs.restaurant_info import RESTAURANT_INFO

def item_exists(item_name):
    for item in RESTAURANT_INFO.dinner_menu:
        if item_name.lower() in item["name"].lower() or item_name.lower() in item["ingredients"].lower():
            return True
    return False

def nationality_exists(nationality):
    if nationality in RESTAURANT_INFO.nationalities:
        return True
    else:
        return False

def load_json(file_path):

    with open(file_path) as f:
        d = json.load(f)
        return (d)