import sqlite3
from chordataweb.ldap.interface import DirectoryServices

"""
Get the list of Tenants for the tenants.db or LDAP services
"""


def get_tenants(configuration: dict) -> list:
    tdb = configuration.get("tenant_database")
    ldap_server = configuration.get("ldap_server_url")
    if tdb is not None:
        db = sqlite3.connect(tdb)
        cursor = db.cursor()
        rows = cursor.execute("SELECT tenant FROM tenants").fetchall()
        rv = []
        for row in rows:
            rv.append(row[0])
        return rv
    elif ldap_server is not None:
        ds = DirectoryServices(configuration)
        ds.connect(
            configuration.get("ldap_bind_user"),
            configuration.get("ldap_bind_password")
        )
        tenant_ous = ds.list_tenants()
        rv = []
        for tenant in tenant_ous:
            rv.append(tenant[0])
        return rv
    return []
