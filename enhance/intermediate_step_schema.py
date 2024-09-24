intermediate_step_schema = {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "name": "given_menu_schema",
     "schema": {
          "type": "array",
          "items": {
               "menu_item": {
                    "type": "object",
                    "properties": {
                         "name": {"type": "string"},
                         "recommended_upsells": { ## enhanced property
                              "type": "array",
                              "description": "An array of recommended menu items to pair with this item.",
                              "items": {
                                   "menu_item": "string",
                              }
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
                         "appeal": {"type": "string"} ## enhanced property
                    },
                    "required": ["name", "recommended_upsells", "narrative", "appeal"],
                    "additionalProperties": False
               }
          },
     },
     "strict": True
}