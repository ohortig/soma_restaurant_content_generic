from inputs.restaurant_info import RESTAURANT_INFO

def item_exists(item_name):
    for item in RESTAURANT_INFO.dinner_menu:
        if item["name"].lower() == item_name.lower():
            return True
    return False

def nationality_exists(nationality):
    if nationality in RESTAURANT_INFO.nationalities:
        return True
    else:
        return False