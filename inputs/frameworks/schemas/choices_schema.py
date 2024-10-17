choices_schema = {
     "name": "choices_response",
     "schema": {
          "type": "object",
          "properties": {
               "choices": {
                    "type": "object",
                    "properties": {
                         "A": {"type": "string"},
                         "B": {"type": "string"},
                         "C": {"type": "string"},
                         "D": {"type": "string"},
                         "correct_answer": {"type": "string"},
                         "explanation": {"type": "string"}
                    },
                    "required": ["A", "B", "C", "D", "correct_answer", "explanation"],
                    "additionalProperties": False,
               }
          },
          "required": ["choices"],
          "additionalProperties": False
     },
     "strict": True
}