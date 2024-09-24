enhanced_menu_schema = {
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
                         "category": {"type": "string"},
                         "name": {"type": "string"},
                         "ingredients": {"type": "string"},
                         "price": {"type": "integer"},
                         "recommended_upsells": {
                              "type": "array",
                              "description": "An array of recommended menu items to pair with this item.",
                              "items": {"$ref": "#/$defs/menu_item"}
                         },
                        "narrative": { ## enhanced property
                              "type": "object",
                              "description": "A narrative about this item catered to each of the three main guest nationalities.",
                              "properties": {
                                   "nationality": {"type": "string"},
                                   "narrative": {"type": "string"}
                                   },
                              "required": ["nationality", "narrative"],
                              "additionalProperties": False
                         },
                         "appeal": {"type": "string"}
                    },
                    "required": ["category", "name", "ingredients", "price", "recommended_upsells", "narrative", "appeal"],
                    "additionalProperties": False
               }
          }
     },
     "strict": True
}