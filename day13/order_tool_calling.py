import sys
import os
from concurrent.futures import ThreadPoolExecutor
from google import genai
from google.genai import types

# --- FIX 1: DYNAMIC PATH RESOLUTION FOR KEY.PY ---
# This eliminates the relative import break and loads key.py flawlessly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import key
from .order_tools import order_tool_registry

# --- FIX 2: TOOL DEFINITION TYPOS FIXED ---
order_status_tool = types.FunctionDeclaration(
    name="get_order_status",
    description="From the given orders data set get the order status for provided the order id",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "order_id": types.Schema(
                type="STRING",
                description="The alphanumeric order id"
            )
        },
        required=["order_id"]
    )
)

order_details_tool = types.FunctionDeclaration(
    name="get_order_details", 
    description="From the given orders data set return the complete order details for the given order id",
    parameters=types.Schema( # Fixed capital 'S'
        type="OBJECT",
        properties={
            "order_id": types.Schema( # Fixed capital 'S'
                type="STRING",       # Fixed 'type' instead of 'types'
                description="The alphanumeric order id"
            )
        },
        required=["order_id"]
    )
)

order_payment_status_tool = types.FunctionDeclaration(
    name="get_payment_status",
    description="From the given orders data set return the order payment status for the given order id",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "order_id": types.Schema(
                type="STRING",
                description="The alphanumeric order id"
            )
        },
        required=["order_id"]      
    )
)

order_shipping_estimate_tool = types.FunctionDeclaration(
    name="get_shipping_estimate",
    description="From the given orders data set return the order shipping estimate for the given order id",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "order_id": types.Schema(
                type="STRING",
                description="The alphanumeric order id"
            )
        },
        required=["order_id"]      
    )
)

orders_tools = types.Tool(
    function_declarations=[
        order_details_tool,
        order_payment_status_tool,
        order_shipping_estimate_tool,
        order_status_tool
    ] 
)

# Make sure API_KEY_NEW is defined inside your key.py file
client = genai.Client(api_key=key.API_KEY_NEW) 
config = types.GenerateContentConfig(tools=[orders_tools])

def query(user_input):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_input,
        config=config
    )
    
    # Check if the model actually wanted to call a tool before running the loop
    if not response.candidates[0].content.parts or not response.candidates[0].content.parts[0].function_call:
        print("Final answer:", response.text)
        return

    tool_responses = []
    thread_results = []
    with ThreadPoolExecutor() as executor:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                print("Function name:", part.function_call.name)
                print("Arguments:", part.function_call.args)
                tool_function = order_tool_registry[part.function_call.name]
                future = executor.submit(tool_function, **part.function_call.args)
                thread_results.append((part.function_call.name, future))
                                
    for function_name, future in thread_results:
        tool_response = types.Part.from_function_response(
            name=function_name,
            response={
                "result": future.result()
            }
        )
        tool_responses.append(tool_response)  
          
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
                parts=tool_responses
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
