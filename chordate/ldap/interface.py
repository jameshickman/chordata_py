import uuid
from string import Template
from ldap3 import Connection, MODIFY_REPLACE, MODIFY_ADD, HASHED_SALTED_SHA
from ldap3.core.exceptions import LDAPBindError
from ldap3.utils.hashed import hashed


def pack_value(v):
    return [(MODIFY_REPLACE, [v])]


class LDAPtemplates:
    admin_user = "cn=${admin},dc=${domain},dc=${tld}"
    ldap_base = "dc=${domain},dc=${tld}"
    user_search = "(uid=${user})"
    user_dn = "uid=${user},cn=People,dc=${domain},dc=${tld}"
    tenant_path = "ou=${tenant},ou=Tenants,dc=${domain},dc=${tld}"
    groups_query = "(member=${user_dn})"
    tenants_base = "ou=Tenants,dc=${domain},dc=${tld}"
    tenants_query = "(&(ou=*)(objectClass=organizationalunit))"
    group_get = "(&(cn=${group})(objectClass=groupOfNames))"
    group = "cn=$group,ou=$tenant,ou=Tenants,dc=${domain},dc=${tld}"
    tenant_group = "(&(ou=${tenant})(objectClass=organizationalunit))"
    user_attributes = ['cn', 'givenName', 'sn', 'telephoneNumber', 'businessCategory']
    tenant_attributes = ['description']


class DirectoryServices:
    server = None
    connection = None
    ldap_base = ""

    def __init__(self, configuration: dict):
        self.config = configuration
        self.ldap_base = Template(LDAPtemplates.ldap_base).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld")
            }
        )
        pass

    def connect(self, user_dn: str, password: str):
        try:
            self.server = self.config.get("ldap_server_url")
            self.connection = Connection(self.server, user=user_dn, password=password, auto_bind=True)
        except LDAPBindError as e:
            return False
        return True

    def activate_connection(self):
        if self.connection is None:
            self.connect(
                self.config.get('ldap_bind_user'),
                self.config.get('ldap_bind_password')
            )
        return

    def list_tenants(self):
        self.activate_connection()
        tenants = []
        tenants_base = Template(LDAPtemplates.tenants_base).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld")
            }
        )
        self.connection.search(
            search_base=tenants_base,
            search_filter=LDAPtemplates.tenants_query,
            attributes=LDAPtemplates.tenant_attributes
        )
        for result in self.connection.entries:
            ent_path = result.entry_dn.split(',')[0]
            ent_name = ent_path.split('=')[1]
            description = result.entry_attributes_as_dict.get('description', [''])
            if len(description) > 0:
                description = description[0]
            if ent_name != "Tenants":
                tenants.append([ent_name, description])
        return tenants

    def get_groups(self, tenant: str, user: str) -> list:
        self.activate_connection()
        roles = []
        tenant_base = Template(LDAPtemplates.tenant_path).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "tenant": tenant
            }
        )
        user_dn = Template(LDAPtemplates.user_dn).substitute(
            {
                "user": user,
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld")
            }
        )
        search_term = Template(LDAPtemplates.groups_query).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "user_dn": user_dn
            }
        )
        self.connection.search(tenant_base, search_term)
        for result in self.connection.entries:
            ent_path = result.entry_dn.split(',')
            ent_type, ent_name = ent_path[0].split('=')
            roles.append(ent_name)
        return roles

    def get_user_data(self, user: str) -> dict:
        self.activate_connection()
        search_term = Template(LDAPtemplates.user_search).substitute({'user': user})
        self.connection.search(
            search_base=self.ldap_base,
            search_filter=search_term,
            attributes=LDAPtemplates.user_attributes
        )
        e = self.connection.entries
        if len(e) > 0:
            return self.connection.entries[0].entry_attributes_as_dict
        return {}

    def update_user_fields(self, user: str, updates: dict):
        self.activate_connection()
        user_dn = Template(LDAPtemplates.user_dn).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "user": user
            }
        )
        u = {}
        for n in updates:
            u[n] = pack_value(updates[n])
        return self.connection.modify(user_dn, u)

    def update_password(self, user: str, password: str):
        self.activate_connection()
        user_dn = Template(LDAPtemplates.user_dn).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "user": user
            }
        )
        hashed_password = hashed(HASHED_SALTED_SHA, password)
        changes = {
            'userPassword': [(MODIFY_REPLACE, [hashed_password])]
        }
        return self.connection.modify(user_dn, changes)

    def user_exists(self, user: str) -> bool:
        self.activate_connection()
        search_term = Template(LDAPtemplates.user_search).substitute({'user': user})
        self.connection.search(self.ldap_base, search_term)
        if len(self.connection.entries) > 0 and self.connection.entries[0]:
            return True
        return False

    def get_users_in(self, tenant: str, group: str) -> dict:
        self.activate_connection()
        tenant_base = Template(LDAPtemplates.tenant_path).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "tenant": tenant
            }
        )
        group_query = Template(LDAPtemplates.group_get).substitute(
            {
                "group": group
            }
        )
        self.connection.search(
            tenant_base,
            group_query,
            attributes=['member']
        )
        return self.connection.entries[0].entry_attributes_as_dict['member']

    def add_user_to(self, tenant: str, user: str, group: str) -> bool:
        self.activate_connection()
        user_dn = Template(LDAPtemplates.user_dn).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "user": user
            }
        )
        group_dn = Template(LDAPtemplates.group).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "tenant": tenant,
                "group": group
            }
        )
        change = {"member": [(MODIFY_ADD, [user_dn])]}
        self.connection.modify(group_dn, change)
        return True

    def create_user(self,
                    email: str,
                    first: str = '',
                    last: str = '',
                    organization: str = '',
                    password: str = None,
                    phone: str = None) -> str:
        self.activate_connection()
        if password is None:
            password = hashed(HASHED_SALTED_SHA, str(uuid.uuid4()))
        user_dn = Template(LDAPtemplates.user_dn).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "user": email
            }
        )
        object_classes = ['inetOrgPerson', 'organizationalPerson', 'person', 'simpleSecurityObject', 'top']
        attributes = {
            'cn': first + ' ' + last,
            'sn': last,
            'userPassword': password,
            'givenName': first,
            'businessCategory': organization
        }
        if phone is not None:
            attributes['telephoneNumber'] = phone
        self.connection.add(user_dn, object_classes, attributes)
        return user_dn

    def tenant_exists(self, tenant_name: str) -> bool:
        self.activate_connection()
        search_term = Template(LDAPtemplates.tenant_group).substitute({'tenant': tenant_name})
        tenant_base = Template(LDAPtemplates.tenants_base).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld")
            }
        )
        self.connection.search(tenant_base, search_term)
        if len(self.connection.entries) > 0 and self.connection.entries[0]:
            return True
        return False

    def test_credentials(self, user_name, password):
        user_dn = Template(LDAPtemplates.user_dn).substitute(
            {
                "domain": self.config.get("ldap_domain"),
                "tld": self.config.get("ldap_tld"),
                "user": user_name
            }
        )
        if self.connect(user_dn, password) is not False:
            # Connect with the Binding user
            self.connect(
                self.config.get("ldap_bind_user"),
                self.config.get("ldap_bind_password")
            )
            return self.get_user_data(user_name)
        return False
