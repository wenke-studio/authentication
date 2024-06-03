from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from server.task import crud, models, schemas

faker = Faker()


def test_list_tasks_view(http: TestClient, db: Session):
    data = {"name": faker.word()}
    task = crud.create_task(db, schemas.TaskCreate(**data))

    response = http.get("/task/v1")
    assert response.status_code == 200

    payload = response.json()
    assert len(payload) == 1
    assert payload[0] == schemas.Task(id=task.id, name=task.name, description=task.description).model_dump()


def test_create_task_view(http: TestClient, db: Session):
    data = {"name": faker.word()}

    response = http.post("/task/v1", json=data)
    assert response.status_code == 201

    payload = response.json()
    task = db.query(models.Task).filter(models.Task.id == payload["id"]).one()
    assert payload["id"] == task.id
    assert payload["name"] == task.name
    assert payload["description"] == task.description


def test_retrieve_task_view(http: TestClient, db: Session):
    data = {"name": faker.word()}
    task = crud.create_task(db, schemas.TaskCreate(**data))

    response = http.get(f"/task/v1/{task.id}")
    assert response.status_code == 200

    payload = response.json()
    assert payload == schemas.Task(id=task.id, name=task.name, description=task.description).model_dump()


def test_update_task_view(http: TestClient, db: Session):
    data = {"name": faker.word()}
    task = crud.create_task(db, schemas.TaskCreate(**data))

    new_data = {"name": faker.word()}
    response = http.put(f"/task/v1/{task.id}", json=new_data)
    assert response.status_code == 200

    db.refresh(task)
    assert task.name == new_data["name"]
    assert task.description is None
