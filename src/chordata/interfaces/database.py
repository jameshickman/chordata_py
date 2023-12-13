class BaseDatabase:
    def __init__(self, tenant, configuration):
        self.tenant = tenant
        self.configuration = configuration
        self._setup()
        pass

    def _setup(self):
        pass

    def get_engine(self):
        pass

    def get_connection(self):
        pass

    def schema_exists(self, schema):
        return False

    def create_schema(self, schema):
        pass

    @staticmethod
    def get_orm_type(self):
        return "UNKNOWN"
