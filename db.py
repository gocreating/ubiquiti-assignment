from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import CreateSchema, DropSchema, MetaData

from config import APP, DB_URL


class Database:

    @staticmethod
    def get_metadata():
        return MetaData(schema=APP)

    def __init__(self, url=None,
                       dialect=None, driver=None, username=None, password=None, host=None, port=None, database=None):
        from models.base import Base

        if not url:
            url = f'{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(url, pool_size=1, echo=False)
        SessionFactory = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.Session = scoped_session(SessionFactory)
        existing_metadata = Database.get_metadata()
        existing_metadata.reflect(bind=self.engine, schema=APP)
        self.existing_metadata = existing_metadata
        self.metadata = Base.metadata

    def drop_schema(self, schema_name):
        self.engine.execute(DropSchema(schema_name))

    def create_schema(self, schema_name):
        self.engine.execute(CreateSchema(schema_name))

    def drop_tables(self):
        self.existing_metadata.drop_all(self.engine)

    def create_tables(self):
        self.metadata.create_all(self.engine)

    def reset(self):
        if self.engine.dialect.has_schema(self.engine, schema=APP):
            self.drop_tables()
            self.drop_schema(APP)
        self.create_schema(APP)
        self.create_tables()

    def get_session(self):
        session = self.Session()
        return session

database = None
if database is None:
    database = Database(url=DB_URL)
