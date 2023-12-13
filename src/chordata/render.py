from airspeed import CachingFileLoader
import jinja2
import json
import os
import pickle
import hashlib
from xml.etree import ElementTree as ET
from chordata.tagbuilder import TagBuilder


class Render:
    def __init__(self,
                 data: dict,
                 meta: dict,
                 working_dir: str,
                 app_name: str,
                 cache_directory):
        self.d = data
        self.d['app'] = app_name
        self.m = meta
        self.wd = working_dir
        self.application = app_name
        self.cache = cache_directory
        return
    
    def render(self):
        code = "200 OK"
        mime = ""
        output = "".encode()
        headers = []
        if 'redirect' in self.m:
            code = "301 Moved Permanently"
            headers.append(('Location', str(self.m['redirect'])))
            headers.append(('Cache-Control', 'no-cache'))
        if 'headers' in self.m:
            headers.extend(self.m['headers'])
        if 'template' in self.m:
            output = ""
            template_type = self.template_type(self.m['template'])
            if template_type == "airstream":
                output = self.render_airstream(self.m['template'], self.d)
            if template_type == "jinja2":
                output = self.render_jinja2(self.m['template'], self.d)
            mime = self.m['type']
        if 'serviceOf' in self.m:
            output = json.dumps(self.d).encode()
            mime = 'text/json'
        if 'raw' in self.m and self.m['raw'] is True:
            output = self.d
            mime = self.m['type']
        if 'etree' in self.m:
            output = self.etree_builder()
            mime = self.m['type']
        return [code, mime, headers, output]

    def render_airstream(self, template: str, data: dict):
        template_base = os.path.join(self.wd, "apps", self.application, "templates")
        loader = CachingFileLoader(template_base)
        template = loader.load_template(os.path.join(template_base, template))
        return template.merge(data, loader=loader).encode()

    def render_jinja2(self, template_file: str, data: dict):
        if template_file.split(os.sep)[0] == "apps":
            base_path = os.path.join(self.wd)
        else:
            base_path = os.path.join(self.wd, "apps", self.application, "templates")
        template_loader = jinja2.FileSystemLoader(searchpath=base_path)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_file)
        return template.render(data).encode()

    @staticmethod
    def template_type(template_file: str):
        ext = template_file.split('.')[-1].lower()
        if ext == "j2" or ext == "jinja2" or ext == "html" or ext == "htm" or ext == "tmpl":
            return "jinja2"
        return "airstream"

    def etree_builder(self) -> str:
        """
        If the meta field 'etree' exists, build an Airstream template and cache.
        Etree is a logical description of the document, use the Element Tree builder
        to realize as an Airstream template and cache.

        'xml': If present and True, override automatic generation of HTML5 generation.

        'etree' structure:
            {
                'tag': 'tag_name',
                'attributes': {'key': 'value', ...}
                'text': 'tag content text',
                'children': [{<recursive structure>}, ...]
            }
        :return: Fully rendered markup
        """
        cache_file = str(hashlib.md5(str(pickle.dumps(self.m.get('etree'))).encode('utf-8')).hexdigest()) + ".tmpl"
        cache_filename = os.path.join(self.cache, cache_file)
        if not os.path.exists(cache_filename):
            self.build_etree_template(cache_filename)
        loader = CachingFileLoader(self.cache)
        template = loader.load_template(os.path.join(self.cache, cache_file))
        return template.merge(self.d, loader=loader).encode()

    def build_etree_template(self, filename):
        def build_tag(source_object: (dict, TagBuilder)) -> ET.Element:
            if isinstance(source_object, TagBuilder):
                source = source_object.get()
            else:
                source = source_object
            if 'attributes' in source:
                el = ET.Element(source.get('tag', 'DIV'), attrib=source['attributes'])
            else:
                el = ET.Element(source.get('tag', 'DIV'))
            if 'text' in source:
                el.text = source['text']
            if 'children' in source:
                for child in source['children']:
                    el.append(build_tag(child))
            return el

        tree = ET.ElementTree(build_tag(self.m['etree']))
        with open(filename, 'w') as f:
            s_output = ""
            if not ('xml' in self.m and self.m['xml'] is True):
                s_output = "<!DOCTYPE html>\n"
            s_output += bytes(ET.tostring(tree.getroot(), encoding='utf8', method='html')).decode("utf-8")
            f.write(s_output)
        return
