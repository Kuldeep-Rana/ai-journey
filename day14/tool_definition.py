from google.genai import types

get_task_by_id_tool = types.FunctionDeclaration(
    name= "getTask",
    description = "Based on the given task id get the task",
    parameters= types.Schema(
        type = "OBJECT",
        properties = {
            "taskId" : types.Schema(
                type = "STRING",
                description = "The alphanumeric id"        
            )
        },
        required = ["taskId"]
    )
)
list_tasks_tool = types.FunctionDeclaration(
    name= "listTasks",
    description = "From the tasks list retrun all the tasks",
    parameters= types.Schema(
        type = "OBJECT",
         properties = {
            "assignee" : types.Schema(
                type = "STRING",
                description = "The string name of the assignee"        
            )
        },
    )
)

task_tools = types.Tool(
    function_declarations = [
        list_tasks_tool,
        get_task_by_id_tool
    ]
)