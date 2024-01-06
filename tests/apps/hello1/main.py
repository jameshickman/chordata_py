from chordataweb.server_env import ServerEnvironment
from chordataweb.response import Response


def index(e: ServerEnvironment, s: dict) -> tuple:
    r = Response({"hello": "world"}).set_template("hello.html")
    return r.build()


def route_vars_test(e: ServerEnvironment, s: dict) -> tuple:
    route_vars = e.get_variables()
    r = Response(
        {
            "var1": route_vars.get("var1", None),
            "var2": route_vars.get("var2", None)
        }
    ).is_json()
    return r.build()


def query_vars_test(e: ServerEnvironment, s: dict) -> tuple:
    q_vars = e.get_query()
    r = Response(
        q_vars
    ).is_json()
    return r.build()
