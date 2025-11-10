from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=300, description="Название задачи")

    status: bool = False

class Task(TaskCreate):
    id: int