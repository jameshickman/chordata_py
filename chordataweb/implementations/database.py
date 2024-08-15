import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from chordataweb.interfaces.database import BaseDatabase
"""
Default implementation using SQLAlchamy and Postgres
"""


class Database(BaseDatabase):
    def _setup(self):
        # Bootstrap SQLAlchamy
        self.conn_string = "postgresql://" + str(self.configuration['database_user']) + ":" + \
                      str(self.configuration['database_password']) + "@" + \
                      str(self.configuration['database_host']) + \
                      ":" + str(self.configuration['database_port']) + "/" + str(self.tenant)
        self.engine = sqlalchemy.create_engine(self.conn_string, echo=False)
        self.session = sessionmaker(bind=self.engine)
        return

    def get_engine(self):
        return self.engine

    def get_connection(self):
        return self.session()

    def schema_exists(self, schema):
        from sqlalchemy.sql import text
        q = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
        statement = text(q)
        conn = self.get_connection()
        r = conn.execute(statement, {"schema": schema}).all()
        conn.close()
        if len(r) > 0:
            return True
        else:
            return False

    def db_exists(self) -> bool:
        return database_exists(self.conn_string)

    def init_database(self) -> bool:
        return create_database(self.conn_string)


    def create_schema(self, schema):
        from sqlalchemy.schema import CreateSchema
        conn = self.get_connection()
        conn.execute(CreateSchema(schema))
        conn.commit()
        conn.close()
        return

    @staticmethod
    def get_orm_type():
        return "SQLAlchamy"
