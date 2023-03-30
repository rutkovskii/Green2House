import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# When running run.py
from app.database.models import Base, User, DataSample
from app.admin.config import ServerConfig

# When running database.py
# from models import Base, User, DataSample
# from admin.config import ServerConfig
# from database_prefills import prefill_users, prefill_samples


engine = sqlalchemy.create_engine(
    ServerConfig.DATABASE_URI)  # Server -> necessary for cron
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@contextmanager
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


def add_sample_users():
    with session_scope() as s:
        s.bulk_save_objects(prefill_users)


def add_example_datasamples():
    with session_scope() as s:
        s.bulk_save_objects(prefill_samples)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # When running database.py
    recreate_database()
    add_sample_users()
    add_example_datasamples()
