import sys
import unittest
import os

"""
Test the handler dispatcher class
"""


class TestDispatcher(unittest.TestCase):
    def setUp(self):
        """
        Set up dummy environment for testing against.
        :return:
        """
        self.wd = os.path.join(os.getcwd())
        pass

    def test_route_loader(self):
        from chordataweb.dispatcher import build_route_map
        routes = build_route_map(self.wd)
        assert isinstance(routes, dict)
        assert isinstance(routes["hello1"]["index"], dict)
        assert isinstance(routes["hello2"]["index"]["permissions"], dict)
        assert isinstance(routes["hello2"]["index"]["permissions"]["post"], list)
        assert routes["hello2"]["index"]["permissions"]["post"][0] == "user"
        assert routes["hello2"]["index"]["permissions"]["delete"][0] == "user"
        assert routes["hello2"]["index"]["permissions"]["delete"][1] == "administrator"
        pass

    def test_permission_tests_open_access(self):
        from chordataweb.dispatcher import build_route_map, Dispatcher
        routes = build_route_map(self.wd)
        d = Dispatcher({'REQUEST_METHOD': 'get'}, {}, routes, "demo",
                       "/hello2/index", self.wd, None, {})
        assert d.permissions_check([]) is True
        assert d.permissions_check(["user"]) is True
        assert d.permissions_check(["user", "administrator"]) is True
        pass

    def test_permission_tests_restricted_post(self):
        from chordataweb.dispatcher import build_route_map, Dispatcher
        routes = build_route_map(self.wd)
        d = Dispatcher({'REQUEST_METHOD': 'post'}, {}, routes, "demo",
                       "/hello2/index", self.wd, None, {})
        assert d.permissions_check([]) is False
        assert d.permissions_check(["user"]) is True
        pass

    def test_permission_tests_restricted_delete(self):
        from chordataweb.dispatcher import build_route_map, Dispatcher
        routes = build_route_map(self.wd)
        d = Dispatcher({'REQUEST_METHOD': 'delete'}, {}, routes, "demo",
                       "/hello2/index", self.wd, None, {})
        assert d.permissions_check([]) is False
        assert d.permissions_check(["user"]) is False
        assert d.permissions_check(["user", "administrator"]) is True
        pass

    def test_route_variables(self):
        from chordataweb.dispatcher import build_route_map, Dispatcher
        routes = build_route_map(self.wd)
        environ = {
            'REQUEST_METHOD': 'get',
            'HTTP_HOST': 'demo.test.com',
            'PATH_INFO': '/hello1/variables/123/test_string'
        }
        d = Dispatcher(environ, {}, routes, "demo",
                       "/hello1/variables/123/test_string", self.wd, None, {})
        data, meta = d.execute(None, {}, {}, '')
        assert data["var1"] == '123'
        assert data['var2'] == 'test_string'
        assert meta['serviceOf'] == 'json'
        pass

    def test_query_vars(self):
        from chordataweb.dispatcher import build_route_map, Dispatcher
        routes = build_route_map(self.wd)
        environ = {
            'REQUEST_METHOD': 'get',
            'HTTP_HOST': 'demo.test.com',
            'PATH_INFO': '/hello1/variables/query',
            'QUERY_STRING': 'var1=123&var2=test_string'
        }
        url = "/hello1/variables/query"
        d = Dispatcher(environ, {}, routes, "demo",
                       url, self.wd, None, {})
        data, meta = d.execute(None, {}, {}, '')
        assert data["var1"] == '123'
        assert data['var2'] == 'test_string'
        assert meta['serviceOf'] == 'json'
        pass
