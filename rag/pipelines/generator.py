from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class JUDGE_LLM:
    JUDGE_SYSTEM_PROMPT = """
    <INSTRUCTIONS>
    You are an AI Expert, specialized in evaluating LLM outputs. 

    You will be given a user_prompt and a LLM_GENERATION couple. This LLM generates questions and answers quiz style from real data provided by user.
    The user_prompt: will include instructions the LLM used to generate the output with real data.
    The LLM_GENERATION: the question and answers generated using the user_prompt data.

    Your task is to provide a 'total rating' scoring how well the llm generates the questions and answers based on the information provided by the user.
    Give your answer on a scale of 1 to 4, where 1 means that the llm_generation is not correct or based on the user context at all, and 4 means that the llm_generation completely and corrctely uses the user_prompt information.
    If you detect that the LLM hallucinates then flag it in your reasoning and reduce score.
    </INSTRUCTIONS>

    <SCALE>
    Here is the scale you should use to build your answer:
    1: The llm_answer is terrible: completely irrelevant to the context user_prompt, or very partial
    2: The llm_answer is mostly not helpful: misses some key aspects of the context of user_prompt
    3: The llm_answer is mostly helpful: provides support, but still could be improved
    4: The llm_answer is excellent: relevant, direct, detailed, and addresses all the concerns raised in the user_prompt
    </SCALE>


    <REQUIREMENTS>
    Provide your feedback as follows:

    Feedback:::
    Evaluation: (your rationale for the rating, as a text)
    Total rating: (your rating, as a number between 1 and 4)
    Reasoning: (short explanation of your evaluation)
    You MUST provide values for 'Evaluation:', 'Total rating:' and 'Reasoning' in your answer.
    </REQUIREMENTS>

    Provide your feedback. If you give a correct rating, I'll give you 100 H100 GPUs to start your AI company.
    Feedback:::
    Evaluation:
    """
    def __init__(self):
        self.openai_model = OpenAI()
        self.parser = StrOutputParser()
        self.history= []

    def save_to_history(self, prompt):
        """Add a new prompt to the context."""
        self.history.append({"role": "user", "content": prompt})

    def format_query(self, USER_PROMPT, LLM_GENERATION):
        """Use it facilitate prompting the judge."""
        QUERY_PROMPT = """
        Evaluate this USER_PROMPT and LLM_GENERATION.

        USER_PROMPT: {USER_PROMPT}
        LLM_GENERATION: {LLM_GENERATION}
        """
        query = QUERY_PROMPT.format(USER_PROMPT=USER_PROMPT, LLM_GENERATION=LLM_GENERATION)
        messages = [
            {"role": "system", "content": self.JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
        return messages
    
    def query_model(self, messages):
        print('Querying model....')
        try:
            completion = self.openai_model.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
                )
            response = completion.choices[0].message.content
            print("QUERY SUCCESS")
            return response
        except Exception as e:
            print("ERROR OPENAI", completion.choices[0].message.refusal)            


