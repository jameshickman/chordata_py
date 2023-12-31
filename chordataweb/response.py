from chordataweb.tagbuilder import TagBuilder


class Response:
    def __init__(self, data):
        self.data = data
        self.meta = {}
        if isinstance(data, bytes) or isinstance(data, bytearray) or hasattr(data, "read"):
            self.meta['raw'] = True

    def is_json(self):
        self.meta['serviceOf'] = 'json'
        return self

    def set_template(self, template: str, mime_type: str = 'text/html'):
        self.meta['template'] = template
        self.meta['type'] = mime_type
        return self

    def set_header(self, name: str, value: str):
        if "headers" not in self.meta:
            self.meta['headers'] = []
        self.meta['headers'].append((name, value))
        return self

    def redirect(self, location: str):
        self.meta['redirect'] = location
        return self

    def set_tag_builder_set(self, etree: TagBuilder, cache_file: str = None, mime_type: str = 'text/html'):
        self.meta['etree'] = etree
        self.meta['type'] = mime_type
        if cache_file is not None:
            self.meta['cache_file'] = cache_file
        return self

    def build(self):
        return self.data, self.meta
