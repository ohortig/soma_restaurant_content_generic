questions_schema = {
    "name": "questions_response",
    "schema": {
        "type": "object",
        "properties": {
            "quiz": {
                "type": "object",
                "properties": {
                    "question1": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question2": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question3": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question4": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question5": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question6": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question7": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question8": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question9": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    },
                    "question10": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    }
                },
                "required": ["question1", "question2", "question3", "question4", "question5", "question6", "question7", "question8", "question9", "question10"],
                "additionalProperties": False
            }
        },
        "required": ["quiz"],
        "additionalProperties": False
    },
    "strict": True
}