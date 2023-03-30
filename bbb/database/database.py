from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

import os

# When running run.py
from database.models import Base, DataSample
from bbb_config import BBB_Config

if not os.path.exists(BBB_Config.DATABASE_LOCATION):
    print("Creating database at: {}".format(BBB_Config.DATABASE_URI))
    engine = create_engine(BBB_Config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


@ contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_unsent_samples(session):
    return session.query(DataSample).filter(DataSample.sent == False).all()


def mark_samples_as_sent(session, samples):
    for sample in samples:
        sample.sent = True
    session.commit()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # When running database.py
    recreate_database()
