from google import genai
import key
from google.genai import types

tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_leave_balance",
            description="Get the remaining leave balance for an employee.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "employee_name": types.Schema(
                        type="STRING",
                        description="The name of the employee."
                    )
                },
                required=["employee_name"]
            )
        )
    ]
)

client = genai.Client(api_key=key.API_KEY_NEW)
config = types.GenerateContentConfig(
    tools=[tool]
)

def get_leave_balance(employee_name):
    employees = {
        "Kuldeep": 12,
        "Rahul": 8,
        "Amit": 15
    }

    return employees.get(employee_name, 0)


def query(user_input):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_input,
        config=config
    )
    #print (response)
    function_call = response.candidates[0].content.parts[0].function_call
    print("Function name:", function_call.name)
    print("Arguments:", function_call.args)

    result = get_leave_balance(function_call.args["employee_name"])
    print(result)
    
     #  Send tool result back to Gemini
    tool_response = types.Part.from_function_response(
        name=function_call.name,
        response={
            "result": result
        }
    )

    #  Ask Gemini to generate the final answer
    final_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_input)
                ]
            ),
            response.candidates[0].content,
            types.Content(
                role="user",
                parts=[tool_response]
            )
        ],
        config=config
    )

    print("Final answer:", final_response.text)


if __name__ == "__main__":
    #print(get_leave_balance("Kuldeep"))
    query("How many leaves does Kuldeep have?")
    
    