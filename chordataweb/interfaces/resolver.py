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

    def domain_verifier(self) -> bool:
        """
        Conduct a DNS lookup for the request hostname.
        Needed to verify that the subdomain specifying the Tenant
        actually exists to prevent host-file based DOS attack
        creating empty databases.
        :return:
        """
        import socket
        host_name = self.e.get('HTTP_X_FORWARDED_HOST')
        returned_ips = list(map(lambda x: x[4][0], socket.getaddrinfo('{}.'.format(host_name),443,type=socket.SOCK_STREAM)))
        if len(returned_ips) > 0:
            return True
        return False
