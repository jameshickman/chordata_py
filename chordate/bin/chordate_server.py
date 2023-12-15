#!/usr/bin/env python3


# Chordata Framework server using extensive IOC Injection
import os
import sys


wd = os.getcwd()
sys.path.append(wd)


from chordate.configuration import env_loader
from chordate.injector import PackageMapper
from chordate.render import Render
from chordate.static import static_file_exists, serve_static
from chordate.dispatcher import Dispatcher, RouteNotFound, build_route_map
from chordate.events import find_watchers
from chordate.cookies import get_cookies, build_cookie_header
from chordate.stderror import e_print
from chordate.output_stream import CHUNK_SIZE, file_buffer

SESSION_COOKIE = "CHORDATASESSION"


configuration_keys = [
    'default_route',
    'session_path',
    'session_timeout',
    'database_user',
    'database_password',
    'database_host',
    'database_port',
    'email_host',
    'email_port',
    'email_user',
    'email_password',
    'email_from',
    'email_secured',
    'user_landing',
    'login',
    'forward_to_var',
    'compile_cache',
    'language_db'
]
configuration = env_loader(configuration_keys)

injection_manager = PackageMapper()

class_map = os.getenv('CHOR_INJECTION_MAP', False)
if class_map is not False:
    injection_manager.load_json(class_map)

# Dynamic mapped packages
Database = injection_manager.get('chordate.implementations.database', 'Database')
SessionManager = injection_manager.get('chordate.implementations.session', 'SessionManager')
ResolveTenant = injection_manager.get('chordate.implementations.resolver', 'ResolveTenant')

# Find all the Application Routes
routes = build_route_map(wd)

# Find any Observers
observers = find_watchers(wd)


def handler(environ, start_response):
    # Apply URI transform to extract the Tenant name and translated URI
    rs = ResolveTenant(environ, configuration)

    # Check if a static file and serve if it resolves
    request_path = rs.get_uri()
    tenant = rs.get_tenant()
    static_file = static_file_exists(wd, request_path, tenant)
    if static_file is not False:
        return serve_static(environ, start_response, static_file)

    if request_path == '/' and 'default_route' in configuration and len(configuration.get('default_route')) > 0:
        start_response("307 Temporary Redirect", [('Location', configuration.get('default_route'))])
        return ["Redirecting to Default".encode()]

    # Attempt to resolve the Route and return 404 if it does not exist
    try:
        dsp = Dispatcher(
            environ,
            configuration,
            routes,
            tenant,
            request_path,
            wd,
            injection_manager,
            observers
        )
    except RouteNotFound:
        start_response("404 Not Found", [])
        return ["Resource does not exist".encode()]

    # Get any active Cookies
    cookies = get_cookies(environ)
    session_id = cookies.get(SESSION_COOKIE, False)

    # Attempt to load an existing Session
    sess = SessionManager(configuration)
    new_session = False
    session_data = {}
    if session_id is False:
        session_id = sess.start()
        new_session = True
    else:
        session_data = sess.get(session_id)
        if session_data is False:
            session_id = sess.start()
            new_session = True
            session_data = {}

    # Check the Permissions on the Route and return 403 if check fails
    if dsp.permissions_check(session_data.get('roles', {}).get(tenant, [])) is False:
        if dsp.pd.isJSON():
            start_response("401 Access Denied", [("Content-Type", "application/json")])
            return ['{"error": "Access Denied"}'.encode()]
        else:
            if "login" in configuration:
                login = configuration.get("login")
                if login is None:
                    login = '/authentication/login'
                forward_to_var = configuration.get("forward_to_var")
                if forward_to_var is None:
                    forward_to_var = ''
                to_login = login + "?" + forward_to_var + "=" + rs.get_raw_uri()
                start_response("307 Temporary Redirect", [('Location', to_login)])
                return ["Redirect to login".encode()]
            start_response("401 Access Denied", [])
        return ["Access denied to Action".encode()]

    # Run the action
    dbc = Database(tenant, configuration)
    try:
        out, meta = dsp.execute(dbc, cookies, session_data, session_id)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        error_message = str(request_path) + "\n" + str(e) + "\n" + tb
        e_print(error_message)
        start_response("500 Internal Server Error", [])
        return ["Unknown problem, see server logs".encode()]

    # Render and return the output of the Action
    app_name = dsp.get_application()
    try:
        code, mime, headers, output = Render(out, meta, wd, app_name, configuration.get('compile_cache')).render()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        error_message = str(request_path) + "\n" + str(e) + "\n" + tb
        e_print(error_message)
        start_response("500 Internal Server Error", [])
        return ["Unable to render output of application action".encode()]
    headers.append(('Content-Type', mime))
    if new_session:
        headers.append(build_cookie_header(SESSION_COOKIE, session_id))
    sess.session_write(session_id, session_data)
    start_response(code, headers)
    if hasattr(output, "read"):
        return file_buffer(output, CHUNK_SIZE)
    else:
        return [output]


def main():
    port = 5000
    if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
        port = int(sys.argv[1])
    from wsgiref.simple_server import make_server
    print("Starting Chordata server on port: " + str(port))
    srv = make_server('localhost', port, handler)
    srv.serve_forever()


if __name__ == "__main__":
    main()
