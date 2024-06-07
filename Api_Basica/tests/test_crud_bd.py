import pytest

from Api_Basica.exceptions import TaskNotFoundError
from Api_Basica.model.model import TaskStatus


def test_create_task(db_instance_empty, session, task1):
    db_instance_empty.create_task(task=task1,session=session)

    tarefa = db_instance_empty.read_task(task_id=1,session=session)

    assert tarefa.title == task1.title
    assert tarefa.description == task1.description
    assert tarefa.status == task1.status


def test_read_all_tasks(db_instance_empty, session, task1, task2):

    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.create_task(task=task2, session=session)

    tasks = db_instance_empty.read_tasks(session=session)
    assert len(tasks) == 2
    assert tasks[0].title == task1.title
    assert tasks[1].title == task2.title


def test_read_all_tasks_bd_empty(db_instance_empty, session, task1, task2):
    tasks = db_instance_empty.read_tasks(session=session)
    assert len(tasks) == 0



def test_delete_task(db_instance_empty, session, task1,task2):
    db_instance_empty.create_task(task=task1,session=session)
    db_instance_empty.create_task(task=task2, session=session)

    db_instance_empty.delete_task(session=session, task_id=1)

    with pytest.raises(TaskNotFoundError):
        db_instance_empty.read_task(task_id=1, session=session)


def teste_delete_all_tasks(db_instance_empty, session, task1, task2):
    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.create_task(task=task2, session=session)

    db_instance_empty.delete_all_tasks(session=session)

    tasks = db_instance_empty.read_tasks(session=session)

    assert len(tasks) == 0


def test_update_task(db_instance_empty, session, task1):
    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.update_task(session=session,task_id=1,task_status=TaskStatus.FINALIZADO, task_title="Tarefa completada")

    task = db_instance_empty.read_task(task_id=1, session=session)

    assert task.status == TaskStatus.FINALIZADO
    assert task.title == "Tarefa completada"
    assert task.updated_at > task.created_at

    assert task.description == task1.description
