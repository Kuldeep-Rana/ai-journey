from google import genai
from google.genai import types

import key
def invoke_api(user_input, temperature):
    config = types.GenerateContentConfig(temperature= temperature)
    client = genai.Client(api_key= key.API_KEY)
    chat = client.chats.create(model= "gemini-3.6-flash", config= config)
    
    response = chat.send_message(user_input)
    print(response.text)
    
def caller(temprature):
    user_input =  input("type your input")
    if not user_input.strip():
        print("Skipping empty input...")
            
    if(user_input.strip().upper() == "END"):
        print("Exiting...")
        return 
    
    invoke_api(user_input, temprature)
    
  
if __name__ == "__main__":
    caller(2)
    
        