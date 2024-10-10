intermediate_step_schema = {
     "name": "given_menu_schema",
     "schema": {
          "type": "object",
          "properties": {
               "menu_items": {
                    "type": "array",
                    "items": {
                         "type": "object",
                         "properties": {
                              "name": {"type": "string"},
                              "recommended_upsells": { ## enhanced property
                                   "type": "array",
                                   "description": "An array of recommended menu items to pair with this item.",
                                   "items": {
                                        "type": "string",
                                   }
                              },
                              "narrative": { ## enhanced property
                                   "type": "object",
                                   "description": "A narrative about this item catered to one of the three main guest nationalities.",
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
          "required": ["menu_items"],
          "additionalProperties": False
     },
     "strict": True
}