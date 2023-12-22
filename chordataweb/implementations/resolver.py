from chordataweb.interfaces.resolver import BaseResolveTenant
"""
Basic implementation of multi-tenancy based on subdomain.
"""


class ResolveTenant(BaseResolveTenant):
    def get_tenant(self):
        host_name = self.e.get('HTTP_HOST')
        subdomain = host_name.split('.')[0]
        return subdomain
