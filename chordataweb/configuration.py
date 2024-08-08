import os


def load_json(pathname: str = None, defaults: dict = None):
    if defaults is None:
        defaults = {}
    import json
    cfg = {}
    if pathname is not None and os.path.exists(pathname):
        with open(pathname, 'r') as fp:
            t = fp.read()
            cfg = json.loads(t)
    return load_os_vars({**defaults, **cfg})


def load_os_vars(configuration: dict) -> dict:
    def process_section(sec: dict) -> dict:
        sec_new = {}
        for k, v in sec.items():
            if isinstance(sec[k], dict):
                sec_new[k] = process_section(sec[k])
            else:
                new_val = sec[k]
                if not str(new_val).isnumeric() and len(str(new_val)) and str(new_val[0]) == '$':
                    new_val = os.environ.get(new_val[1:])
                    if new_val == 'true' or new_val == 'yes':
                        sec_new[k] = True
                    elif new_val == 'false' or new_val == 'no':
                        sec_new[k] = False
                    else:
                        sec_new[k] = new_val
                else:
                    sec_new[k] = v
        return sec_new
    return process_section(configuration)
