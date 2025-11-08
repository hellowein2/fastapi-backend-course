from fastapi import FastAPI, Body
from storage import JSONStorage, CloudJSONStorage
from models import Task, TaskCreate
import os
from dotenv import load_dotenv
from clients import CloudFlareClient

app = FastAPI()

load_dotenv()
BIN_ID = os.getenv('BIN_ID')
MASTER_KEY = os.getenv('MASTER_KEY')
storage = CloudJSONStorage(bin_id=BIN_ID, master_key=MASTER_KEY)

API_TOKEN_AI = os.getenv('API_TOKEN_AI')
ACCOUNT_ID_AI = os.getenv('ACCOUNT_ID_AI')
client_ai = CloudFlareClient(API_TOKEN_AI, ACCOUNT_ID_AI)


@app.get("/tasks")
def get_tasks():
    return storage.get_task()

@app.post("/tasks")
def create_task(task_data: TaskCreate):
    ai_reply = client_ai.generate_answer(task_data.title)
    task_data.title = f"{task_data.title} — {ai_reply}"
    task = storage.create_task(task_data.model_dump())
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskCreate = Body(...)):
    ai_reply = client_ai.generate_answer(task_data.title)
    task_data.title = f"{task_data.title} — {ai_reply}"
    is_update = storage.update_task(task_id, task_data.model_dump())
    if is_update: return is_update
    return None

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    is_delete = storage.delete_task(task_id)
    if is_delete: return True
    return None
