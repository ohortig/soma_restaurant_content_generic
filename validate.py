from inputs.restaurant_info.nationalities import nationalities
from inputs.menus.given_menu import given_menu

def item_exists(item_name):
    for item in given_menu:
        if item["name"].lower() == item_name.lower():
            return True
    return False

def nationality_exists(nationality):
    if nationality in nationalities:
        return True
    else:
        return False