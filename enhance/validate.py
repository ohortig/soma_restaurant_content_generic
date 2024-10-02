def dish_exists(menu, dish_name):
    print(f"Checking {dish_name} existence...")
    for item in menu:
        if item["name"].lower() == dish_name.lower():
            print(f"\t{dish_name} existence validated.")
            return True
    return False

def dish_exists_in_menu(menu, dish_name):
    # supposing menu is full text
    if dish_name in menu:
        return True
    return False