import json
from pathlib import Path
import requests

class IsMemoryStorage:

    def __init__(self):
        self.tasks = []
        self.next_task = 1


    def list_tasks(self):
        return self.tasks

    def create_task(self, task_data):
        task = {'id': self.next_task, **task_data}
        self.tasks.append(task)
        self.next_task += 1

        return task

    def get_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def update_task(self, task_id:int, task_data):
        for task in self.tasks:
            if task['id'] == task_id:
                task.update(task_data)
                return task
        return None


    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if not task: return False
        self.tasks.remove(task)
        return True


class JSONStorage:
    def __init__(self, filepath: str | None = "tasks.json"):
        self.file = Path(filepath)
        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")

    def _load(self):
        with self.file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_task(self):
        return self._load()

    def create_task(self, task_data: dict):
        tasks = self._load()
        new_id = max([t["id"] for t in tasks], default=0) + 1
        task = {"id": new_id, **task_data}
        tasks.append(task)
        self._save(tasks)
        return task

    def update_task(self, task_id: int, new_data: dict):
        tasks = self._load()
        for task in tasks:
            if task["id"] == task_id:
                task.update(new_data)
                self._save(tasks)
                return task
        return None

    def delete_task(self, task_id: int):
        tasks = self._load()
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                self._save(tasks)
                return task
        return None

class CloudJSONStorage(JSONStorage):
    def __init__(self, bin_id: str, master_key: str):
        super().__init__(filepath="tasks.json")
        self.base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            "X-Master-Key": master_key,
            "Content-Type": "application/json",
        }

    def _load(self):
        res = requests.get(f"{self.base_url}/latest", headers=self.headers)
        res.raise_for_status()
        record = res.json()["record"]
        return record.get("tasks", [])

    def _save(self, tasks):
        payload = {"tasks": tasks}
        res = requests.put(self.base_url, headers=self.headers, json=payload)
        res.raise_for_status()
        return res.json()
