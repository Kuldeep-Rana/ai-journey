from google import genai
from  key  import API_KEY_NEW
from google.genai import types
from .tools import tool_registry
from .tool_definition import task_tools

client = genai.Client(api_key=API_KEY_NEW)
config = types.GenerateContentConfig(tools=[task_tools])
import sys

def query(user_input):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_input,
        config=config
    )
    if not response.candidates[0].content.parts or not response.candidates[0].content.parts[0].function_call:
            print("Final answer:", response.text)
            return
    
    tool_parts = []   
        
    for part in response.candidates[0].content.parts:
        if part.function_call:
            print("Function name:", part.function_call.name)
            print("Arguments:", part.function_call.args)
            tool_function = tool_registry[part.function_call.name]
            result = tool_function(**part.function_call.args)        
            tool_parts.append(
                types.Part.from_function_response(
                    name=part.function_call.name,
                    # The response object must be a dictionary or protocol message
                    response={"result": result} 
                )
            )
     
    final_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_input)]
                ),
                response.candidates[0].content,
                types.Content(
                    role="user", 
                    parts=tool_parts
                )
            ],
            config=config
        )
    
    print("Final answer:", final_response.text)        

if __name__ == "__main__":
    while True:
        prompt = input("Type your input: ")
        if prompt == "END":
            sys.exit(0)
            
        query(prompt)     
     