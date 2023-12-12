import sys


def e_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
