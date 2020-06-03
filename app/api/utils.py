from app import engine
from sqlalchemy.orm import Session


def get_session():
    return Session(engine)


def get_serializable_session():
    session = Session(engine)
    session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
    return session
