#!/usr/bin/env python3
"""
Chordate Chron task manager
"""

import os
import sys
import time
import threading
import random
from chordataweb.configuration import env_loader
from chordataweb.interval import find_chron_configurations, ChronParams
from chordataweb.tenants import get_tenants
from chordataweb.injector import PackageMapper
from chordataweb.stderror import e_print
from chordataweb.interfaces.database import BaseDatabase


class RunHandler(threading.Thread):
    def __init__(self,
                 Database: BaseDatabase,
                 app_dir: str,
                 package: str,
                 function: str,
                 tenant: str,
                 configuration: dict,
                 now: float):
        threading.Thread.__init__(self)
        self.dbc = Database(tenant, configuration)
        self.app_dir = app_dir
        self.package = package
        self.function = function
        self.tenant = tenant
        self.configuration = configuration
        self.now = now
        pass

    def run(self):
        pkg = __import__(self.package, fromlist=[self.function])
        getattr(pkg, self.function)(
            ChronParams(
                self.dbc,
                self.tenant,
                self.app_dir,
                self.configuration,
                self.now
            )
        )
        return


def main():
    injection_manager = PackageMapper()
    class_map = os.getenv('CHOR_INJECTION_MAP', False)
    if class_map is not False:
        injection_manager.load_json(class_map)
    Database = injection_manager.get('chordataweb.implementations.database', 'Database')
    wd = os.getcwd()
    sys.path.append(wd)
    configuration = env_loader(
        [
            'tenant_database',
            'ldap_server_url',
            'ldap_domain',
            'ldap_tld',
            'ldap_bind_user',
            'ldap_bind_password',
            'database_host',
            'database_port',
            'database_user',
            'database_password',
            'email_host',
            'email_port',
            'email_user',
            'email_password',
            'email_from',
            'email_secured',
            'language_db'
        ]
    )
    jobs = find_chron_configurations(wd)
    tenants = get_tenants(configuration)
    now = time.time()
    for i in range(0, len(jobs)):
        if "next" not in jobs[i].keys():
            jobs[i]['next'] = now + float(random.randint(0, 20))
    while True:
        now = time.time()
        for tenant in tenants:
            for chron in jobs:
                if chron['next'] <= now:
                    app_dir = os.path.join(wd, "apps", chron['app'])
                    chron['next'] = now + chron['interval']
                    package = "apps." + chron['app'] + "." + chron['package']
                    function = chron['function']
                    try:
                        RunHandler(Database, app_dir, package, function, tenant, configuration, now).start()
                    except Exception as e:
                        e_print(str(e))
        time.sleep(1)


if __name__ == '__main__':
    main()
