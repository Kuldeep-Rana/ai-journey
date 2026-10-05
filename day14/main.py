from google import genai
from  key  import API_KEY_NEW
from google.genai import types
from .tools import tool_registry
from .tool_definition import task_tools

client = genai.Client(api_key=API_KEY_NEW)
config = types.GenerateContentConfig(tools=[task_tools])
import sys

MAX_STEPS = 5

def query(user_input):

    # 1. Maintain conversation history
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input)
            ]
        )
    ]

    # 2. First call
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config
    )

    # 3. Tool-calling loop
    for i in range(MAX_STEPS):

        function_calls = [
            part
            for part in response.candidates[0].content.parts
            if part.function_call
        ]

        # 4. No function call → final answer
        if not function_calls:
            print("Final answer:", response.text)
            return

        # 5. Add Gemini's response to conversation history
        contents.append(response.candidates[0].content)

        tool_parts = []

        # 6. Execute requested tools
        for part in function_calls:

            print("Function name:", part.function_call.name)
            print("Arguments:", part.function_call.args)

            tool_function = tool_registry[part.function_call.name]

            result = tool_function(**part.function_call.args)

            tool_parts.append(
                types.Part.from_function_response(
                    name=part.function_call.name,
                    response={"result": result}
                )
            )

        # 7. Add tool results to conversation history
        contents.append(
            types.Content(
                role="user",
                parts=tool_parts
            )
        )

        # 8. Ask Gemini again using the FULL history
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=config
        )

    print("Unable to complete the request within the allowed steps.")
    
if __name__ == "__main__":
    while True:
        prompt = input("Type your input: ")
        if prompt == "END":
            sys.exit(0)
            
        query(prompt)     
     