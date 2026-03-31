class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")


class UserNotFoundError(Exception):
    def __init__(self, identifier):
        super().__init__(f"User '{identifier}' not found")


class DuplicateUserError(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username '{username}' already exists")


class InvalidCredentialsError(Exception):
    def __init__(self):
        super().__init__("Invalid username or password")
