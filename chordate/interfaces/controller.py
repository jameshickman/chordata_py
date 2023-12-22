"""
Base Controller

Provides an interface to Controller logic for encapsulation and easier testing.

Business logic is intentionally decoupled from the server environment
for testing purposes. Data is packed into a simple dictionary. Models
are derived from ModelBase and so can be implemented as mock database
objects.

Models are assigned to class properties that are the class name in
all lower case.
"""


class BaseController:
    def __init__(self, session: dict, configuration: dict, models: list):
        self.session = session
        self.configuration = configuration
        for model in models:
            class_name = str(type(model).__name__)
            setattr(self, class_name.lower(), model)
        pass

    def run(self, data: dict, verb: str = 'get'):
        verb = verb.lower()
        if verb == 'get':
            return self.do_get(data)
        elif verb == 'head':
            return self.do_head(data)
        elif verb == 'post':
            return self.do_post(data)
        elif verb == 'put':
            return self.do_put(data)
        elif verb == 'delete':
            return self.do_delete(data)
        elif verb == 'connect':
            return self.do_connect(data)
        elif verb == 'options':
            return self.do_options(data)
        elif verb == 'trace':
            return self.do_trace(data)
        elif verb == 'patch':
            return self.do_trace(data)
        elif verb == 'job':
            return self.do_recurring_job(data)
        else:
            return self._default(data)
        pass

    def do_get(self, data: dict):
        return self._default(data)

    def do_head(self, data: dict):
        return self._default(data)

    def do_post(self, data: dict):
        return self._default(data)

    def do_put(self, data: dict):
        return self._default(data)

    def do_delete(self, data: dict):
        return self._default(data)

    def do_connect(self, data: dict):
        return self._default(data)

    def do_options(self, data: dict):
        return self._default(data)

    def do_trace(self, data: dict):
        return self._default(data)

    def do_patch(self, data: dict):
        return self._default(data)

    def do_recurring_job(self, data: dict):
        return self._default(data)

    def _default(self, data: dict):
        raise Exception("Default Controller logic not implemented.")
