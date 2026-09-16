from google import genai
import key
from google.genai import types
from tools import tools_registry
import sys

leave_balance_tool = types.FunctionDeclaration(
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

employee_department_tool = types.FunctionDeclaration(
    name="get_employee_department",
    description="Get the department of an employee.",
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

get_company_holidays_tool = types.FunctionDeclaration(
    name = "get_company_holidays",
    description= "Get company holidays",

)

get_company_holidays_tool_by_year = types.FunctionDeclaration(
    name = "get_company_holidays_by_year",
    description= "Get company holidays for a given year",
    parameters=types.Schema(
        type = "OBJECT",
        properties={
            "year" : types.Schema(
                type= "INTEGER",
                description= "Get the company holiday list for a specific calendar year. Use this when the user asks about company holidays for a particular year."
            )
        },
        required= ["year"]
    )

)

tool = types.Tool(
    function_declarations=[ 
        leave_balance_tool,
        employee_department_tool,
        get_company_holidays_tool,
        get_company_holidays_tool_by_year]
)

client = genai.Client(api_key=key.API_KEY_NEW)
config = types.GenerateContentConfig(
    tools=[tool]
)

def query(user_input):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_input,
        config=config
    )
    tool_responses = []
    #print (response)
    for part in response.candidates[0].content.parts:
        print("Function name:", part.function_call.name)
        print("Arguments:", part.function_call.args)
        tool_function = tools_registry[part.function_call.name]
        #result = tool_function(function_call.args["employee_name"]) -- limited to employee name
        result = tool_function(**part.function_call.args) # This ** automatically takes care of args to be binded based on the method signature
        print(result)
        
        #  Send tool result back to Gemini
        tool_response = types.Part.from_function_response(
            name=part.function_call.name,
            response={
                "result": result
            }
        )
        tool_responses.append(tool_response)

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
                parts=tool_responses
            )
        ],
        config=config
    )

    print("Final answer:", final_response.text)


if __name__ == "__main__":
    #print(get_leave_balance("Kuldeep"))
    while(True):
        prompt = input("Type your input:")
        if(prompt == "END"):
            sys.exit(1)
            
        query(prompt)    
    
    