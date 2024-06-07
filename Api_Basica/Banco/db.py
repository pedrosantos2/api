import os
from typing import List
from datetime import datetime, timezone
from sqlmodel import SQLModel, create_engine, Session, select
from Api_Basica.model.model import Tasks, TaskStatus
from logger import create_logger
from exceptions import TaskNotFoundError

filename = os.path.splitext(os.path.basename(__file__))[0]

logger = create_logger(logger_name=filename)


class DB:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db")
        SQLModel.metadata.create_all(self.engine)

    def create_task(self, task: Tasks, session: Session) -> None:
        logger.info('Criando tarefa do BD')
        session.add(task)
        session.commit()

    def read_task(self, task_id: int, session: Session) -> Tasks:
        logger.info(f"Lendo tarefa {task_id} do BD")
        comando = select(Tasks).where(Tasks.id == task_id)
        result: Tasks = session.exec(comando).first()
        if result:
            return result
        else:
            logger.error("Task não encontrada")
            raise TaskNotFoundError(f"Task com o ID {task_id} não encontrada")

    def read_tasks(self, session: Session) -> List[Tasks]:
        logger.info("Lendo TODAS as tarefas do BD")
        comando = select(Tasks)
        results = session.exec(comando)
        return [r for r in results]

    def update_task(self, session: Session, task_id: str, task_title: str = None, task_description: str = None,
                    task_status: TaskStatus = None, ) -> None:
        logger.info(f"Alterando a task {task_id} no BD")
        comando = select(Tasks).where(Tasks.id == task_id)
        result = session.exec(comando).first()

        if result:
            if task_title:
                result.title = task_title

            if task_description:
                result.description = task_description

            if task_status:
                result.status = task_status

            updated_at = datetime.now(timezone.utc)
            result.updated_at = updated_at

            session.add(result)
            session.commit()
            logger.info(f"Task com id {task_id} alterada no BD")

        else:
            logger.error(f"Task com ID {task_id} não alterada")
            raise TaskNotFoundError(f"Task com id {task_id} não encontrada")

    def delete_task(self, session: Session, task_id: int) -> None:
        logger.info(f"Deletando task {task_id} no BD")
        comando = select(Tasks).where(Tasks.id == task_id)
        results = session.exec(comando)
        task = results.first()

        if task:
            session.delete(task)
            session.commit()
        else:
            logger.error(f"Task com id {task_id} não encontrada")
            raise TaskNotFoundError(f"Task com id {task_id} não encontrada")

    def delete_all_tasks(self, session: Session) -> None:
        logger.info("Deletando TODAS as tarefas do BD")
        comando = select(Tasks)
        results = session.exec(comando)

        if results:
            for task in results:
                session.delete(task)
                session.commit()
        else:
            logger.error(f"Não foram encontradas Tasks")
            raise TaskNotFoundError("Não foram encontradas tasks")
