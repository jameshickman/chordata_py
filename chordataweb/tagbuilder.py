class TagBuilder:
    def __init__(self, tag: str = 'div'):
        self.d = {
            'tag': tag
        }
        pass

    def add_attributes(self, attr: dict):
        """
        Add a dictionary of attributes to the tracked attributes.
        :param attr:
        :return:
        """
        if 'attributes' not in self.d:
            self.d['attributes'] = {}
        self.d['attributes'] = {**self.d['attributes'], **attr}
        return self

    def add_data(self, attr: dict):
        """
        Same as above, but prefix the field name with "data-" as per the
        HTML standard for user defined data attributes.
        :param attr:
        :return:
        """
        if 'attributes' not in self.d:
            self.d['attributes'] = {}
        attr_new = {}
        for k in attr:
            attr_new['data-' + str(k)] = attr[k]
        self.d['attributes'] = {**self.d['attributes'], **attr_new}
        return self

    def set_text(self, text: str):
        self.d['text'] = text
        return self

    def add_child(self, child: ('TagBuilder', list)):
        def flatten(inp: list) -> list:
            o = []
            for item in inp:
                if isinstance(item, list):
                    o.extend(flatten(item))
                else:
                    o.append(item)
            return o
        if 'children' not in self.d:
            self.d['children'] = []
        if isinstance(child, TagBuilder):
            self.d['children'].append(child)
        else:
            if len(child) > 0:
                self.d['children'].extend(flatten(child))
        return self

    def get(self) -> dict:
        return self.d
