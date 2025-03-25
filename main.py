from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import datetime
import json

OPENAI_API_KEY = ""
# Initialize FastAPI
app = FastAPI()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=OPENAI_API_KEY,
)

# Request model for AI modification
class Todo(BaseModel):
    id: int
    taskName: str
    priority: int
    dueDate: datetime.datetime
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
class TodoRequest(BaseModel):
    user_prompt: str
    todo_list: list[Todo]


# OpenAI API call function
def modify_todo_list(user_prompt: str, todo_list: list[Todo]):
    prompt_text = f"""
    You are an AI assistant that helps manage a to-do list. Given a user's prompt and their current to-do list, update it accordingly.

    User Prompt: "{user_prompt}"
    Current To-Do List: {todo_list}
    Today's Date: {datetime.datetime.now().isoformat()}

    Provide the modified to-do list as a json and do not use any other text only json and do not use back.
    Also, when adding a new to-do use the format 
    taskName: str
    priority: int
    dueDate: Timestamp in ISO 8601 format.
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant for managing to-do lists."},
            {"role": "user", "content": prompt_text}
        ],
        model = "gpt-4o",
        temperature = 1,
        max_tokens = 4096,
        top_p = 1

    )
    return response.choices[0].message.content

# API Endpoint
@app.post("/modify-todo")
def modify_todo(request: TodoRequest):
    try:
        updated_list = modify_todo_list(request.user_prompt, request.todo_list)
        return {"updated_todo_list": json.loads(updated_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
