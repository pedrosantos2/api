from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    NAO_INICIADO = "Não Iniciado"
    EM_PROGRESSO = "Em Progresso"
    FINALIZADO = "Finalizado"

class Tasks(SQLModel, table=True):
    id:  Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Id da tarefa"
    )

    title: str = Field(description="O titulo da tarefa")
    description: str = Field(description="A descrição da tarefa")
    status: TaskStatus = Field(sa_column_kwargs={"default": TaskStatus.NAO_INICIADO}, description="O status da tarefa")

    created_at: datetime = Field(
        default = datetime.now(timezone.utc),
        nullable=False,
        description="Momento da criação da tarefa"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        description="Momento da edição da tarefa"

    )

