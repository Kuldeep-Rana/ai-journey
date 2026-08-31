from google import genai
import key

SOURCE_OF_TRUTH = """

Company Refund Policy

1. Customers can request a refund within 14 days of purchase.

2. Digital products become non-refundable once downloaded.

3. Annual subscriptions may be canceled at any time, but refunds are only available within the first 14 days.

4. Refund processing may take up to 7 business days.
"""

def check(user_input):
    promtpt = f"""
        Answer the user's question using only the policy below.

        If the answer is not supported by the policy, say:
        "Insufficient information."

        POLICY:
        {SOURCE_OF_TRUTH}
        
        QUESTION:
        {user_input}
    """
    
    client = genai.Client(api_key=key.API_KEY)
    chat = client.chats.create(model="gemini-3.6-flash")
    response = chat.send_message(promtpt)
    print(response.text)
    
def readInput():
    while (True):
        user_input = input("Type input:")
        if user_input.strip().upper() == "END":
            break
        check(user_input)
        
if __name__ == "__main__":
    readInput()