from google import genai
from google.genai import types
import key


def invoke_api(user_input, temperature, topP, topK):
    config = types.GenerateContentConfig(temperature= temperature, top_k=topK, top_p= topP)
    client = genai.Client(api_key= key.API_KEY)
    chat = client.chats.create(model= "gemini-3.6-flash", config= config)
    
    response = chat.send_message(user_input)
    print(response.text)


def caller(temprature, topP, topK):
    user_input =  input("type your input")
    if not user_input.strip():
        print("Skipping empty input...")
            
    if(user_input.strip().upper() == "END"):
        print("Exiting...")
        return 
    
    invoke_api(user_input, temprature, topP, topK)
    
  
if __name__ == "__main__":
    caller(1.0, 0.80, 10)
