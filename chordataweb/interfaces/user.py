class BaseUser:
    def __init__(self, configuration):
        self.configuration = configuration
        pass

    def test_credentials(self, username: str, password: str, passthrough=False):
        return False

    def in_tenant(self, tenant):
        return False

    def user_data(self):
        return {}

    def get_roles(self, tenant: str):
        return []

