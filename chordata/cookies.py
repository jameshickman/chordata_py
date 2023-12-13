def build_cookie_header(name: str, value: str, days=365) -> tuple:
    import datetime
    dt = datetime.datetime.now() + datetime.timedelta(days=days)
    fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    secs = days * 86400
    return 'Set-Cookie', '{}={}; Expires={}; Max-Age={}; Path=/'.format(name, value, fdt, secs)


def cookie_kill_header(name: str) -> str:
    return 'Set-Cookie', '{}=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/'.format(name)


def get_cookies(environ) -> dict:
    cookie_values = {}
    c = environ.get("HTTP_COOKIE")
    if c is not None:
        cookies = str(c).split('; ')
        for cookie in cookies:
            parts = str(cookie).split('=')
            cookie_values[parts[0]] = parts[1]
    return cookie_values
