"""
Wrapper around the TagBuilder system for efficient cached compiled templates.

Generation timestamp embedded in the cache filename.

The call-back for build() should be a handwritten builder that builds the top-level
HTML constructs. Needs to accept the Translation object, dictionary of included
sections, stylesheets and scripts.

Return the metadata 'etree' the result of calling build() and 'cache_file' the result
of calling get_template_name()

'event_source' items need to be handled by a handler that if passed the integer timestamp returns
True if the generation timestamp is newer than the current template, else false.

If passed a dictionary containing the properties 'app' the app name and 'translation' the Translation
object.
"""
import hashlib
import glob
import os
import time
from typing import Callable

from chordataweb.tagbuilder import TagBuilder
from chordataweb.util.translation import Translate
from chordataweb.events import EventManager


class TagCache:
    def __init__(self, configuration: dict, app_name: str, interface_name: str, language_code: str = "en_us"):
        self.configuration = configuration
        self.app_name = app_name
        self.interface_name = interface_name
        self.language_code = language_code
        self.signature = str(hashlib.md5(str(app_name + interface_name).encode("utf-8")).hexdigest())
        self.existing_template = None
        self.template_timestamp = 0
        self.template_exists = False
        """
        Check if an existing cached template exists and deletes outdated templates.
        :return:
        """
        find_path = os.path.join(
            self.configuration.get('compile_cache'), self.signature + "-*-" + self.language_code + ".vtpl"
        )
        templates = glob.glob(find_path)
        if len(templates) > 0:
            self.template_exists = True
            timestamps = []
            newest_timestamp = 0
            for template in templates:
                ts = int(template.split('/')[-1].split(".")[0].split("-")[1])
                if ts > newest_timestamp:
                    newest_timestamp = ts
                timestamps.append(ts)
            for timestamp in timestamps:
                if timestamp != newest_timestamp:
                    to_delete = os.path.join(
                        self.configuration.get('compile_cache'),
                        self.signature + "-" + str(timestamp) + ".vtpl"
                    )
                    os.remove(to_delete)
            self.existing_template = self.signature + "-" + str(newest_timestamp) + "-" + self.language_code + ".vtpl"
            self.template_timestamp = newest_timestamp

    def get_timestamp(self) -> int:
        return self.template_timestamp

    def get_template_name(self) -> str:
        if self.existing_template is not None:
            return self.existing_template
        else:
            self.template_timestamp = int(time.time())
            self.existing_template = self.signature + "-" + str(
                self.template_timestamp) + "-" + self.language_code + ".vtpl"
            return self.existing_template

    def build(self,
              event_manager: EventManager,
              source_events: list,
              root_timestamp: int,
              root_builder: Callable,
              local_includes: list = None
              ) -> (None, TagBuilder):
        t = Translate(self.language_code, self.configuration.get('language_db'))
        dirty = False
        if self.template_exists and root_timestamp > self.template_timestamp:
            dirty = True
        else:
            for event in source_events:
                rvs = event_manager.send(event, self.template_timestamp)
                for hdl in rvs:
                    if rvs[hdl] is not False:
                        dirty = True
                        break
                if dirty is True:
                    break
        if dirty or not self.template_exists:
            includes = {}
            stylesheets = []
            scripts = []
            if local_includes is not None:
                includes = local_includes
            for event in source_events:
                includes[event] = []
                rvs = event_manager.send(event, {'app': self.app_name, 'translation': t})
                returned_interfaces = []
                for hdl in rvs:
                    returned_interfaces.append(rvs[hdl])
                returned_interfaces = sorted(returned_interfaces, key=lambda d: d['weight'])
                for interface in returned_interfaces:
                    includes[event].append(interface.get('interface'))
                    if 'stylesheets' in interface:
                        stylesheets.extend(interface.get('stylesheets'))
                    if 'scripts' in interface:
                        scripts.extend(interface.get('scripts'))
            return root_builder(t, includes, set(stylesheets), set(scripts))
        return None
