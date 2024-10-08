quiz_json_schema = {
    "name": "quiz_response",
    "schema": {
        "type": "object",
        "properties": {
            "Quiz": {
                "type": "object",
                "properties": {
                    "question1": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question2": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question3": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type", "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question4": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question5": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question6": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question7": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question8": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type", "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question9": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    },
                    "question10": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"},
                            "correct_answer": {"type": "string"},
                            "answer_explanation": {"type": "string"}
                        },
                        "required": ["question", "A", "B", "C", "D", "correct_answer", "answer_explanation"],
                        "additionalProperties": False
                    }
                },
                "required": ["question1", "question2", "question3", "question4", "question5", "question6", "question7", "question8", "question9", "question10"],
                "additionalProperties": False
            }
        },
        "required": ["Quiz"],
        "additionalProperties": False
    },
    "strict": True
}