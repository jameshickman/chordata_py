from chordate.interfaces.resolver import BaseResolveTenant
import sqlite3
"""
Complex resolver that does not depend on the domain name.

The URI must start with a name or number, that is resolved against a
SQLite database so number or name can be accepted. URI is the full
request with the tenant identifier stripped off.

Required configuration:
tenant_database - full path to the SQLite database with the Tenants mapping. 
"""


def url_resolver(uri: str, database_file: str) -> dict:
    parts = uri.split('/')
    tenant = parts[1]
    if not tenant.isnumeric():
        if tenant[0] != '_':
            return {
                'tenant': '',
                'uri': uri
            }
        else:
            tenant = tenant[1:]
    rv = {
        'tenant': '',
        'uri': ''
    }
    uri_translated = '/' + '/'.join(parts[2:])
    is_mt = True
    db = sqlite3.connect(database_file)
    cur = db.cursor()
    if tenant.isnumeric():
        """
        Need to fetch the name from the database
        """
        row = cur.execute("SELECT tenant FROM tenants WHERE id = ?", (int(tenant), )).fetchone()
        if row is None:
            is_mt = False
        rv['tenant'] = row[0]
    else:
        row = cur.execute("SELECT COUNT(*) FROM tenants WHERE tenant = ?", (str(tenant), )).fetchone()
        if row[0] == 0:
            is_mt = False
        else:
            rv['tenant'] = tenant
    if is_mt:
        rv['uri'] = uri_translated
    else:
        rv['uri'] = uri
    return rv


class ResolveTenant(BaseResolveTenant):
    def __init__(self, environ, configuration: dict):
        super().__init__(environ, configuration)
        self.resolved = url_resolver(self.u, configuration.get('tenant_database'))

    def get_tenant(self):
        return self.resolved['tenant']

    def get_uri(self):
        return self.resolved['uri']

    def get_raw_uri(self):
        qs = self.e.get('QUERY_STRING', '')
        if qs != '':
            return self.resolved['uri'] + '?' + qs
        else:
            return self.resolved['uri']
