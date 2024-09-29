def dish_exists(menu, dish_name):
    print(f"Checking {dish_name} existence...")
    for item in menu:
        if item["name"].lower() == dish_name.lower():
            print(f"\t{dish_name} existence validated.")
            return True
    return False