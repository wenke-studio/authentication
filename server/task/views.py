import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from server.core.database import get_db
from server.core.schemas import HTTPError, HTTPSuccess

from . import crud, schemas

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/task/v1",
    tags=["Task"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Task],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        }
    },
)
def list_tasks(db: Session = Depends(get_db)):
    try:
        tasks = crud.list_tasks(db)
        return tasks
    except SQLAlchemyError as exc:
        logging.error("Error creating task: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task",
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Task,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        }
    },
)
def create_task(
    task_create: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    try:
        task = crud.create_task(db, task_create)
        return task
    except SQLAlchemyError as exc:
        logging.error("Error creating task: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task",
        )


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Task,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "model": HTTPError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        },
    },
)
def retrieve_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = crud.retrieve_task(db, task_id)
        return task
    except NoResultFound as exc:
        logging.error("Task not found: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    except SQLAlchemyError as exc:
        logging.error("Error retrieving task: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving task",
        )


@router.put(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "model": HTTPError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        },
    },
)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    try:
        crud.update_task(db, task_id, task_update)
        return {"detail": "Task updated"}
    except NoResultFound as exc:
        logging.error("Task not found: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    except SQLAlchemyError as exc:
        logging.error("Error updating task: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task",
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "model": HTTPError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        },
    },
)
def destroy_task(task_id: int, db: Session = Depends(get_db)):
    try:
        crud.destroy_task(db, task_id)
        return {"detail": "Task deleted"}
    except NoResultFound as exc:
        logging.error("Task not found: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    except SQLAlchemyError as exc:
        logging.error("Error deleting task: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting task",
        )
