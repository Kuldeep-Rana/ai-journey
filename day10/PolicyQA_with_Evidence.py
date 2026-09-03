from pydantic import BaseModel
from typing import Literal

from google import genai
from google.genai import types
import key
import time
POLICY = """COMPANY POLICY

Leave Policy:
Employees receive 24 days of paid leave per calendar year.
Unused leave can be carried forward up to a maximum of 10 days.

Remote Work Policy:
Employees can work remotely up to 2 days per week.
Remote work requires manager approval.

Expense Policy:
Business travel expenses must be submitted within 30 days
after the completion of the trip."""


class PolicyAnswer(BaseModel):
    answer: str
    status: Literal[
        "SUPPORTED",
        "CONTRADICTED",
        "INSUFFICIENT_INFORMATION"
    ]
    evidence: list[str]
    
def call_api(question):
    input = f"""    
        You are a company policy assistant.
        Answer the user's question using ONLY the provided company policy.
        
        Rules:
        1. Do not use outside knowledge.
        2. Do not invent policies.
        3. Every factual claim in the answer must be supported by the policy.
        4. If the policy explicitly disagrees with the user's claim,
        return CONTRADICTED.
        5. If the policy does not contain enough information,
        return INSUFFICIENT_INFORMATION.
        6. Provide the exact policy statement(s) that support your answer
        in the evidence field.
        7. If there is no supporting evidence, return an empty evidence list.

        COMPANY POLICY:
        {POLICY}

        USER QUESTION:
        {question}
    """

    client = genai.Client(api_key= key.API_KEY)
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PolicyAnswer,
    )
    chat = client.chats.create(model="gemini-3.6-flash", config= config)
    response = chat.send_message(input)

    structured_data = PolicyAnswer.model_validate_json(response.text)
    
    print("--- Verified Object Output ---")
    print(f"Answer: {structured_data.answer}")
    print(f"Evidence: {structured_data.evidence}")
    print(f"Status:  {structured_data.status}")
    
if __name__ == "__main__":
    
    inputs = ["How many paid leave days do employees receive per year?", "How many days can I work remotely per week?",
              "How much parental leave do employees receive?","The policy says employees can work remotely 5 days per week, right?"]
    
    for input in inputs:
        print(f"Question: {input}")
        call_api(input)         
        
        print("                          ")
        time.sleep(5)