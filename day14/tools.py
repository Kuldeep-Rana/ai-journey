import json
from pathlib import Path

script_dir = Path(__file__).parent
file_path = script_dir /  "tasks.json"

def listTasks(assignee: str = None):
    with open(file_path, "r", encoding = "UTF-8") as file: 
        tasks = json.load(file)    
    if assignee:
        return [task for task in tasks if task.get("assignee", "").lower() == assignee.lower()]
    return tasks



def getTask(taskId):
    tasks = listTasks()
    
    for task in tasks:
        if (task.get("id") == taskId):
            return task
    
    return {"error": f"No task found for task if {taskId}"}
    


tool_registry = {
    "listTasks": listTasks,
    "getTask" : getTask
}
 
 
