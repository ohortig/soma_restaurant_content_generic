given_menu_schema = {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "name": "given_menu_schema",
     "schema": {
          "type": "array",
          "items": {
               "$ref": "#/$defs/menu_item"
          },
          "$defs": {
               "menu_item": {
                    "type": "object",
                    "properties": {
                         "category": {
                              "type": "string",
                         },
                         "name": {
                              "type": "string",
                         },
                         "ingredients": {
                              "type": "string",
                         },
                         "price": {
                              "type": "integer",
                         }
                    },
                    "required": ["category", "name", "ingredients", "price"],
                    "additionalProperties": False
               }
          }
     },
     "strict": True
}