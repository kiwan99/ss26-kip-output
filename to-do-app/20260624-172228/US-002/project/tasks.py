class Task:
    def __init__(self, description):
        self.id = id(self)
        self.description = description
        self.done = False

    def __repr__(self):
        return f"Task(id={self.id}, description='{self.description}', done={self.done})"

class Tasks:
    def __init__(self):
        self.tasks = []

    def add(self, description):
        self.tasks.append(Task(description))

    def get_all(self):
        return self.tasks

    def mark_done(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.done = True
                break