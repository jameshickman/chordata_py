import os
import json
from chordata.posts import POSTdata
from chordata.events import EventManager
from chordata.server_env import ServerEnvironment
from chordata.stderror import e_print


def build_route_map(working_directory: str):
    route_map = {}
    apps_directory = os.path.join(working_directory, "apps")
    for app_dir in os.listdir(apps_directory):
        if os.path.isdir(os.path.join(apps_directory, app_dir)):
            if os.path.exists(os.path.join(apps_directory, app_dir, "routes.json")):
                route_map[app_dir] = get_json_data(os.path.join(apps_directory, app_dir, "routes.json"))
    return route_map


def get_json_data(pathname):
    with open(pathname, 'r') as fp:
        t = fp.read()
    return json.loads(t)


class RouteNotFound(Exception):
    def __init__(self, route):
        self.route = route
        pass

    def __str__(self):
        return self.route


class Dispatcher:
    def __init__(
            self,
            wsgi_environ,
            configuration: dict,
            route_map: dict,
            tenant_name: str,
            request_path: str,
            working_directory: str,
            injector,
            watcher_map
    ):
        self.map = route_map
        self.environ = wsgi_environ
        self.pd = POSTdata(self.environ)
        self.verb = str(self.environ.get('REQUEST_METHOD', '')).lower()
        self.configuration = configuration
        self.tenant = tenant_name
        self.working_directory = working_directory
        self.watcher_map = watcher_map
        self.injector = injector
        path_parts = str(request_path).split('/')
        self.application = path_parts[1]
        self.request_path = '/'.join(path_parts[2:])
        self.key = ''
        found = False
        for k in route_map.get(self.application, []):
            if self._match_check(self.request_path, k):
                self.key = k
                found = True
                break
        if not found:
            raise RouteNotFound(self.request_path)
        pass

    def permissions_check(self, user_roles: list = []):
        if ('permissions' not in self.map[self.application][self.key] or
                len(self.map[self.application][self.key]['permissions']) == 0):
            return True
        permissions = self.map[self.application][self.key]['permissions']
        if isinstance(permissions, dict):
            if self.verb in list(dict(permissions).keys()):
                to_test_against = permissions[self.verb]
            else:
                to_test_against = permissions.get('default')
                if to_test_against is None:
                    return False
        else:
            to_test_against = permissions
        if len(to_test_against) == 0:
            return True
        for required in to_test_against:
            if required not in user_roles:
                return False
        return True

    def get_application(self):
        return self.application

    def execute(
            self,
            database,
            cookies: dict = {},
            session: dict = {},
            session_id: str = ''
    ):
        self._setup_check(database)
        package_name = "apps." + str(self.application) + '.' + str(self.map[self.application][self.key]['package'])
        function_name = str(self.map[self.application][self.key]['function'])
        params = ServerEnvironment(
            self.environ,
            self.configuration,
            cookies,
            self.get_full_url(),
            database,
            self.tenant,
            os.path.join(self.working_directory, 'apps', self.application),
            self.injector,
            self._extract_route_vars(self.request_path, self.key),
            self._query_vars(),
            EventManager(self.watcher_map, self.application, database),
            session_id
        )
        params.set_verb(self.verb)
        if self.pd.isPost():
            params.set_data_type('POST')
            params.set_post_data(self.pd)
        if self.pd.isJSON():
            params.set_data_type('JSON')
            params.set_json_data(self.pd.getJSON())
        package = __import__(package_name, fromlist=[function_name])
        return getattr(package, function_name)(params, session)

    def get_full_url(self):
        qs = self.environ.get('QUERY_STRING', '')
        url = "https://" + str(self.environ['HTTP_HOST']) + str(self.environ['PATH_INFO'])
        if qs != '':
            url = url + "?" + qs
        return url

    def _setup_check(self, database):
        setup_package = "apps." + str(self.application) + ".setup"
        try:
            setup = __import__(setup_package, fromlist=['schema', 'setup'])
            fn_schema_name = getattr(setup, "schema")
            fn_setup = getattr(setup, "setup")
            schema = fn_schema_name()
            if not database.schema_exists(schema):
                fn_setup(database)
        except ImportError:
            pass
        except AttributeError as e:
            e_print(e)
            pass
        return

    def _query_vars(self):
        q_vars = {}
        qs = self.environ.get('QUERY_STRING', '')
        var_pairs = qs.split('&')
        for var in var_pairs:
            if var == '':
                return {}
            k, v = var.split('=')
            q_vars[k] = v
        return q_vars

    @staticmethod
    def _match_check(url: str, key: str):
        segments_url = url.split('/')
        segments_key = key.split('/')
        if len(segments_url) != len(segments_key):
            return False
        matched = True
        idx = 0
        for k in segments_key:
            is_var = False
            if k[0] == '{':
                is_var = True
            if idx > len(segments_url):
                matched = False
                break
            if not is_var and segments_url[idx] != k:
                matched = False
                break
            idx += 1
        return matched

    @staticmethod
    def _extract_route_vars(url: str, signature: str):
        values = {}
        segments_url = url.split('/')
        segments_sig = signature.split('/')
        idx = 0
        for d in segments_sig:
            if d[0] == '{':
                name = d[1:-1]
                values[name] = segments_url[idx]
            idx += 1
        return values
