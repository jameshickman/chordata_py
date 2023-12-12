class PackageMapper:
    def __init__(self, package_map: dict = {}):
        self.map = package_map
        pass

    def get(self, name: str):
        if name in self.map:
            package_name = self.map[name]
        else:
            package_name = name
        return __import__(package_name)

    def get(self, name, import_name: str):
        if name in self.map:
            package_name = self.map[name]
        else:
            package_name = name
        pkg = __import__(package_name, fromlist=[import_name])
        return getattr(pkg, import_name)

    def load_json(self, pathname):
        """
        Load a JSON file of maps and merge it into the Map of packages
        :param pathname:
        :return:
        """
        import json
        try:
            with open(pathname, 'r') as fp:
                t = fp.read()
                new_map = json.loads(t)
                self.map = {**self.map, **new_map}
        except FileNotFoundError as e:
            return False
        return True
