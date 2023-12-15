import os
import json
from chordate.interfaces.database import BaseDatabase
from chordate.stderror import e_print


class EventParams:
    def __init__(self,
                 database: BaseDatabase,
                 frm: str,
                 em: 'EventManager',
                 payload):
        self.database = database
        self.frm = frm
        self.event_manager = em
        self.payload = payload
        pass

    def get_database(self) -> BaseDatabase:
        return self.database

    def get_from(self) -> str:
        return self.frm

    def get_payload(self):
        return self.payload

    def get_event_manager(self):
        return self.event_manager


def find_watchers(working_directory: str):
    watcher_map = {}
    apps_directory = os.path.join(working_directory, "apps")
    for app_dir in os.listdir(apps_directory):
        observer_file = os.path.join(working_directory, "apps", app_dir, "observers.json")
        if os.path.exists(observer_file):
            try:
                with open(observer_file, 'r') as fp:
                    map_data = json.loads(fp.read())
                    watcher_map[app_dir] = map_data
            except Exception as e:
                e_print(str(e))
                pass
    return watcher_map


class EventManager:
    def __init__(self, watchers: dict, app: str, database: BaseDatabase):
        self.map = watchers
        self.app = app
        self.database = database
        pass

    def send(self, event_name: str, payload=None) -> dict:
        rv = {}
        for dest in self.map:
            if event_name in self.map[dest]:
                package = "apps." + str(dest) + "." + str(self.map[dest][event_name]['package'])
                function = str(self.map[dest][event_name]['function'])
                pkg = __import__(package, fromlist=[function])
                rv[dest] = getattr(pkg, function)(
                    EventParams(
                        self.database,
                        self.app,
                        self,
                        payload
                    )
                )
        return rv
