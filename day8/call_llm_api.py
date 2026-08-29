from google import genai
import key

def call_api(user_input):
    
    client = genai.Client(api_key= key.API_KEY)
    chat = client.chats.create(model="gemini-3.6-flash")
    response = chat.send_message(user_input)

    print(response.text)


def caller() :
    for i in range(0,10):
        user_input =  input("type your input")
        if not user_input.strip():
            print("Skipping empty input...")
            continue
        
        if(user_input == "END"):
            break
        
        call_api(user_input)

if __name__ == "__main__":
    caller()
    
        