class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        super().__init__(f"Task with id {task_id} not found")
        self.task_id = task_id


class UserNotFoundError(Exception):
    def __init__(self, identifier):
        super().__init__(f"User '{identifier}' not found")
        self.identifier = identifier


class DuplicateUserError(Exception):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")
        self.username = username
