


from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str
    status: bool

tasks_db = []
task_id_counter = 1

@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}/", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    task_dict = task.dict()
    task_dict["id"] = task_id_counter
    task_id_counter += 1
    tasks_db.append(task_dict)
    return task_dict

@app.put("/tasks/{task_id}/", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_db[task_index].update(updated_task.dict())
    return tasks_db[task_index]

@app.delete("/tasks/{task_id}/", response_model=Task)
def delete_task(task_id: int):
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted_task = tasks_db.pop(task_index)
    return deleted_task
