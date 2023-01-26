import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

## When running run.py
from app.models import Base, User, DataSample
from app.admin.config import ServerConfig

## When running database.py
# from models import Base, User, DataSample
# from admin.config import ServerConfig
# from database_prefills import prefill_users, prefill_samples



engine = sqlalchemy.create_engine(
    ServerConfig.DATABASE_URI)  # Server -> necessary for cron
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def add_sample_users():
    s = Session()
    s.bulk_save_objects(prefill_users)
    s.commit()
    s.close()


def add_example_datasamples():
    s = Session()
    s.bulk_save_objects(prefill_samples)
    s.commit()
    s.close()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

#    with session_scope() as s:
        # s.add(book)


if __name__ == "__main__":
    # When running database.py
    recreate_database()
    add_sample_users()
    add_example_datasamples()

    pass
