from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    status: bool

class Task(TaskCreate):
    id: int