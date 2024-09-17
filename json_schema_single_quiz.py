json_schema = {
    "name": "quiz_response",
    "schema": {
        "type": "object",
        "properties": {
            "Cycle 1": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "Quiz 1": {
                            "type": "object",
                            "properties": {
                                "question1": {
                                    "type": "object",
                                    "properties": {
                                        "menu_knowledge_question_1": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["menu_knowledge_question_1", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question2": {
                                    "type": "object",
                                    "properties": {
                                        "menu_knowledge_question_2": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["menu_knowledge_question_2", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question3": {
                                    "type": "object",
                                    "properties": {
                                        "menu_knowledge_question_3": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["menu_knowledge_question_3", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question4": {
                                    "type": "object",
                                    "properties": {
                                        "tricks_and_tips_question_1": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["tricks_and_tips_question_1", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question5": {
                                    "type": "object",
                                    "properties": {
                                        "tricks_and_tips_question_2": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["tricks_and_tips_question_2", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question6": {
                                    "type": "object",
                                    "properties": {
                                        "tricks_and_tips_question_3": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["tricks_and_tips_question_3", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question7": {
                                    "type": "object",
                                    "properties": {
                                        "wine_upselling_question_1": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["wine_upselling_question_1", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question8": {
                                    "type": "object",
                                    "properties": {
                                        "cultural_competency_question_1": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["cultural_competency_question_1", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question9": {
                                    "type": "object",
                                    "properties": {
                                        "problem_solving_question_1": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["problem_solving_question_1", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                },
                                "question10": {
                                    "type": "object",
                                    "properties": {
                                        "food_safety_question_1": {"type": "string"},
                                        "A": {"type": "string"},
                                        "B": {"type": "string"},
                                        "C": {"type": "string"},
                                        "D": {"type": "string"},
                                        "correct_answer": {"type": "string"}
                                    },
                                    "required": ["food_safety_question_1", "A", "B", "C", "D", "correct_answer"],
                                    "additionalProperties": False
                                }
                            },
                            "required": ["question1", "question2", "question3", "question4", "question5", "question6", "question7", "question8", "question9", "question10"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["Quiz 1"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["Cycle 1"],
        "additionalProperties": False
    },
    "strict": True
}