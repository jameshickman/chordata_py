from chordataweb.server_env import ServerEnvironment
from chordataweb.response import Response


def index(e: ServerEnvironment, s: dict) -> tuple:
    r = Response({"hello": "world"}).set_template("hello.html")
    return r.build()
