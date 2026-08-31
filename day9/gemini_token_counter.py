from google import genai
import key
def count():
    client = genai.Client(api_key= key.API_KEY)
    
    interaction1 = client.interactions.create(
        model="gemini-3.6-flash",
        input="Hi, my name is kuldeep"
    )

    interaction2 = client.interactions.create(
        model="gemini-3.6-flash",
        input="What's my name?",
        previous_interaction_id=interaction1.id
    )

    print(f"Input tokens: {interaction2.usage.total_input_tokens}")
    print(f"Output tokens: {interaction2.usage.total_output_tokens}")
    print(f"Total tokens: {interaction2.usage.total_tokens}")
   
if __name__ == "__main__":
    count();