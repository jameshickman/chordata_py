#!/usr/bin/env python3
"""
Chordate Chron task manager
"""

import os
import sys
import time
from chordate.configuration import env_loader
from chordate.interval import find_chron_configurations, ChronParams
from chordate.tenants import get_tenants
from chordate.injector import PackageMapper
from chordate.stderror import e_print


def main():
    injection_manager = PackageMapper()
    class_map = os.getenv('CHOR_INJECTION_MAP', False)
    if class_map is not False:
        injection_manager.load_json(class_map)
    Database = injection_manager.get('chordate.implementations.database', 'Database')
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
    for i in range(0, len(jobs)):
        if "next" not in jobs[i].keys():
            jobs[i]['next'] = 0
    while True:
        now = time.time()
        for tenant in tenants:
            dbc = Database(tenant, configuration)
            for chron in jobs:
                if chron['next'] <= now:
                    app_dir = os.path.join(wd, "apps", chron['app'])
                    chron['next'] = now + chron['interval']
                    package = "apps." + chron['app'] + "." + chron['package']
                    function = chron['function']
                    try:
                        pkg = __import__(package, fromlist=[function])
                        getattr(pkg, function)(ChronParams(dbc, tenant, app_dir, configuration, now))
                    except Exception as e:
                        e_print(str(e))
        time.sleep(1)


if __name__ == '__main__':
    main()
