import os
import json
from chordate.stderror import e_print
from chordate.interfaces.database import BaseDatabase


def find_chron_configurations(working_directory: str) -> list:
    chron_list = []
    apps_directory = os.path.join(working_directory, "apps")
    for app_dir in os.listdir(apps_directory):
        chron_config_file = os.path.join(working_directory, "apps", str(app_dir), "chron.json")
        if os.path.exists(chron_config_file):
            try:
                with open(chron_config_file, "r") as chron_file:
                    chron_json_txt = chron_file.read()
                    chron_json = json.loads(chron_json_txt)
                    for i in range(0, len(chron_json)):
                        chron_json[i]['app'] = app_dir
                    chron_list.extend(chron_json)
            except Exception as e:
                e_print(str(e))
    return chron_list


class ChronParams:
    def __init__(self, database: BaseDatabase, tenant: str, app_dir: str, configuration: dict, time_stamp: float):
        self.database = database
        self.tenant = tenant
        self.app_dir = app_dir
        self.configuration = configuration
        self.time_stamp = time_stamp
        pass

    def get_database(self) -> BaseDatabase:
        return self.database

    def get_tenant(self) -> str:
        return self.tenant

    def get_app_dir(self) -> str:
        return self.app_dir

    def get_configuration(self) -> dict:
        return self.configuration

    def get_time_stamp(self) -> float:
        return self.time_stamp
