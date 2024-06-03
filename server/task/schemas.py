from __future__ import annotations

from pydantic import BaseModel, model_validator


class TaskCreate(BaseModel):
    """Task create schema

    Args:
        name (str): taskname
        description (str, optional): task description. Defaults to None.
    """

    name: str
    description: str | None = None


class TaskUpdate(BaseModel):
    """Task update schema

    Args:
        name (str, optional): task name. Defaults to None.
        description (str, optional): task description. Defaults to None.
    """

    name: str | None = None
    description: str | None = None

    @model_validator(mode="after")
    def check_at_least_one(self) -> TaskUpdate:
        conditions = [self.name is None, self.description is None]
        if all(conditions):
            raise ValueError("At least one field is required, `title` or `description`")
        return self


class Task(TaskCreate):
    """Task schema

    Args:
        id (int): task id
        title (str): task title
        description (str, optional): task description. Defaults to None.
    """

    id: int

    class Config:
        from_attributes = True
