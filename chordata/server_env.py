from chordata.interfaces.database import BaseDatabase
from chordata.injector import PackageMapper
from chordata.events import EventManager
from chordata.posts import POSTdata


class ServerEnvironment:
    def __init__(self,
                 environment: dict,
                 configuration: dict,
                 cookies: dict,
                 url: str,
                 database: BaseDatabase,
                 tenant: str,
                 working_directory: str,
                 injector: PackageMapper,
                 variables: dict,
                 query: dict,
                 events: EventManager,
                 session_id: str
                 ):
        self.environment = environment
        self.configuration = configuration
        self.cookies = cookies
        self.url = url
        self.database = database
        self.tenant = tenant
        self.working_directory = working_directory
        self.injector = injector
        self.variables = variables
        self.query = query
        self.events = events
        self.session_id = session_id
        self.data_type = 'GET'
        self.post = None
        self.data = None
        self.verb = ''
        pass

    def get_environment(self) -> dict:
        return self.environment

    def get_configuration(self) -> dict:
        return self.configuration

    def get_cookies(self) -> dict:
        return self.cookies

    def get_url(self) -> str:
        return self.url

    def get_database(self) -> BaseDatabase:
        return self.database

    def get_tenant(self) -> str:
        return self.tenant

    def get_working_directory(self) -> str:
        return self.working_directory

    def get_injection_manager(self) -> PackageMapper:
        return self.injector

    def get_variables(self) -> dict:
        return self.variables

    def get_query(self) -> dict:
        return self.query

    def get_event_manager(self) -> EventManager:
        return self.events

    def get_session_id(self) -> str:
        return self.session_id

    def get_data_type(self) -> str:
        return self.data_type

    def get_data(self) -> (dict, POSTdata):
        return self.data

    def set_data_type(self, t: str):
        self.data_type = t

    def set_post_data(self, pd: POSTdata):
        self.data = pd

    def set_json_data(self, d: dict):
        self.data = d

    def set_verb(self, verb: str):
        self.verb = verb

    def get_verb(self) -> str:
        return self.verb

