from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from . import models, schemas


def list_tasks(db: Session) -> list[models.Task]:
    """Return a list of all tasks in the database

    Args:
        db (Session): SQLAlchemy session

    Returns:
        list[models.Task]: List of all tasks in the database

    Raises:
        SQLAlchemyError: If there is an error in the database
    """
    return db.query(models.Task).all()


def create_task(db: Session, task_create: schemas.TaskCreate) -> models.Task:
    """Create a task

    Args:
        db (Session): SQLAlchemy session
        task_create (schemas.TaskCreate): Task data to create

    Returns:
        models.Task: The created task

    Raises:
        SQLAlchemyError: If there is an error in the database
    """
    data = task_create.model_dump(exclude_none=True)
    task = models.Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def retrieve_task(db: Session, task_id: int) -> models.Task:
    """Retrieve a task

    Args:
        db (Session): SQLAlchemy session
        task_id (int): Task ID

    Returns:
        models.Task: The task found with the ID

    Raises:
        NoResultFound: If no task is found with the ID
        MultipleResultsFound: If more than one task is found with the ID
    """
    result = db.query(models.Task).filter(models.Task.id == task_id)
    return result.one()


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate) -> models.Task:
    """Update a task

    Args:
        db (Session): SQLAlchemy session
        task_id (int): Task ID
        task_update (schemas.TaskUpdate): Task data to update

    Returns:
        models.Task: The updated task

    Raises:
        NoResultFound: If no task is found with the ID
    """
    affected_rows = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .update(
            task_update.model_dump(exclude_none=True),
        )
    )
    if affected_rows == 0:
        raise NoResultFound(f"No task found with the ID {task_id}")
    db.commit()
    return affected_rows


def destroy_task(db: Session, task_id: int) -> int:
    """Delete a task

    Args:
        db (Session): SQLAlchemy session
        task_id (int): Task ID

    Returns:
        int: Number of affected rows

    Raises:
        NoResultFound: If no task is found with the ID
    """
    affected_rows = db.query(models.Task).filter(models.Task.id == task_id).delete()
    if affected_rows == 0:
        raise NoResultFound(f"No task found with the ID {task_id}")
    db.commit()
    return affected_rows
