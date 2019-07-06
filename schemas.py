from app import ma
from models import Client, Project, Task


class ClientSchema(ma.Schema):
    class Meta:
        model = Client


client_schema = ClientSchema(strict=True)
clients_schema = ClientSchema(many=True, strict=True)


class ProjectSchema(ma.Schema):
    class Meta:
        model = Project


project_schema = ProjectSchema(strict=True)
projects_schema = ProjectSchema(many=True, strict=True)


class TaskSchema(ma.Schema):
    class Meta:
        model = Task


task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(many=True, strict=True)
