class BaseResolveTenant:
    def __init__(self, environ, configuration: dict = None):
        self.e = environ
        self.u = environ.get('PATH_INFO')
        self.config = configuration
        pass

    def get_tenant(self):
        """
        Override with specific logic to extract the Tenant name from subdomain, part of the URI or
        any other applicable technique.
        :return:
        """
        pass

    def get_uri(self):
        """
        If the request URI is modified by extracting a Tenant field or simular override with required logic.
        :return:
        """
        return self.u

    def get_raw_uri(self):
        """
        Return the complete request and query string
        :return:
        """
        qs = self.e.get('QUERY_STRING', '')
        if qs != '':
            return self.u + '?' + qs
        else:
            return self.u

