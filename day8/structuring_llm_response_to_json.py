from pydantic import BaseModel
from typing import Literal

from google import genai
from google.genai import types

import key
class TicketAnalysis(BaseModel):
    issue_category : Literal["DUPLICAE_PAYMENT","PAYMENT_FAILED","PAYMENT_SUCCESSFUL", "INVOICE_ACCESS","APPLICATION_CRASH", "OTHER"]
    priority: Literal ["0","1", "2", "3", "4"]
    summary : str
    
def call_api():
    input = "My account was charged twice and I cannot access the invoice."
    #input = "The application crashes whenever I try to upload a PDF."
    client = genai.Client(api_key= key.API_KEY)
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TicketAnalysis,
    )
    chat = client.chats.create(model="gemini-3.6-flash", config= config)
    response = chat.send_message(input)

    structured_data = TicketAnalysis.model_validate_json(response.text)
    
    print("--- Verified Object Output ---")
    print(f"Category: {structured_data.issue_category}")
    print(f"Priority: {structured_data.priority}")
    print(f"Summary:  {structured_data.summary}")
    
if __name__ == "__main__":
    call_api()     