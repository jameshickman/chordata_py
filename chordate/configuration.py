import os


def load_json(pathname: str, defaults: dict = {}):
    import json
    try:
        with open(pathname, 'r') as fp:
            t = fp.read()
            cfg = json.loads(t)
            defaults = {**defaults, **cfg}
    except FileNotFoundError:
        return False
    return defaults


def env_loader(defs: list):
    defs.extend(dynamic_key_loader())
    cfg = {}
    for d in defs:
        cfg[d] = os.getenv("CHOR_" + str(d))
    return cfg


def dynamic_key_loader() -> list:
    v = []
    extra_keys = os.getenv('CHOR_custom_keys')
    if isinstance(extra_keys, str):
        v = extra_keys.split(':')
    return v
