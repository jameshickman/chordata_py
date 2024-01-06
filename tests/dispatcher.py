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
        os.environ['REQUEST_METHOD'] = "get"
        self.wd = os.path.join(os.getcwd(), "cases")
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
