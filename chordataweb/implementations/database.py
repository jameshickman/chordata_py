import sqlalchemy
from sqlalchemy.orm import sessionmaker

from chordataweb.interfaces.database import BaseDatabase
"""
Default implementation using SQLAlchamy and Postgres
"""


class Database(BaseDatabase):
    def _setup(self):
        # Bootstrap SQLAlchamy
        conn_string = "postgresql://" + str(self.configuration['database_user']) + ":" + \
                      str(self.configuration['database_password']) + "@" + \
                      str(self.configuration['database_host']) + \
                      ":" + str(self.configuration['database_port']) + "/" + str(self.tenant)
        self.engine = sqlalchemy.create_engine(conn_string, echo=False)
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

    def create_schema(self, schema):
        from sqlalchemy.schema import CreateSchema
        self.engine.execute(CreateSchema(schema))
        return

    @staticmethod
    def get_orm_type(self):
        return "SQLAlchamy"
