import pytest
from sqlmodel import Session
from Api_Basica.Banco.db import DB
from Api_Basica.model.model import Tasks, TaskStatus


@pytest.fixture
def task1():
    task1 = Tasks(
        title="Ir na academia",
        description="Preciso me exercitar 09:00h",
        status=TaskStatus.NAO_INICIADO
    )
    yield task1


@pytest.fixture
def task2():
    task2 = Tasks(
        title="Marcar Médico",
        description="Preciso recuperar minha visão...",
        status=TaskStatus.EM_PROGRESSO
    )
    yield task2


@pytest.fixture
def db_instance(scope="session"):
    db = DB()
    yield db


@pytest.fixture
def session(db_instance, scope="session"):
    session = Session(db_instance.engine)
    yield session
    session.close()


@pytest.fixture
def db_instance_empty(db_instance, session, scope="session"):
    # limpa o banco antes dos testes
    db_instance.delete_all_tasks(session=session)
    yield db_instance
    # limpa o banco depois dos testes
    db_instance.delete_all_tasks(session=session)
