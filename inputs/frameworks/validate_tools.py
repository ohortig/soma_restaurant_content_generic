validate_call_tools = [
     {
        "type": "function",
        "function": {
            "name": "item_exists",
            "strict": True,
            "description": "Find out if the given item_name string exists in the menu. item_name is the name, and only the name, of an item referenced in a quiz question. It is not a basic ingredient, but an entire dish, meal, or drink.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name, and only the name, of the item referenced in a quiz question. item_exists then checks if item_name exists in the menu.",
                    },
                },
                "required": ["item_name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nationality_exists",
            "strict": True,
            "description": "Find out if the given nationality string exists in the nationalities list. nationalities is the name, and only the name, of a nationality referenced in a quiz question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nationality": {
                        "type": "string",
                        "description": "The name, and only the name, of a nationality referenced in a quiz question. nationality_exists then checks if the nationality exists in the nationalities list.",
                    },
                },
                "required": ["nationality"],
                "additionalProperties": False,
            },
        }
    },
]