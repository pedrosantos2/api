import os
from sqlmodel import Session
from database.db import DB
from logger import create_logger
from model.model import Tasks, TaskStatus

filename = os.path.splitext(os.path.basename(__file__))[0]

logger = create_logger(logger_name=filename)

if __name__ == "__main__":
    task1 = Tasks(
        title="Ir na academia",
        description="Preciso me exercitar 09:00h",
        status=TaskStatus.NAO_INICIADO,

    )

    task2 = Tasks(
        title="Estudar testes de SW",
        description="Preciso recuperar aquele 4...",
        status=TaskStatus.NAO_INICIADO
    )

    db = DB()

    session = Session(db.engine)

    db.create_task(task=task1, session=session)
    db.create_task(task=task2, session=session)

    task = db.read_task(task_id=2, session=session)
    print(task.description)

    tasks = db.read_tasks(session=session)
    for task in tasks:
        print(task.title)

    db.update_task(
        session=session,
        task_id=1,
        task_status=TaskStatus.FINALIZADO,
    )

    task = db.read_task(task_id=1, session=session)
    print(task.status)

    db.delete_task(session=session, task_id=1)
    task = db.read_task(task_id=1, session=session)
    print(task.status)

    db.delete_all_tasks(session=session)
    task = db.read_task(task_id=2, session=session)
    print(task.status)
