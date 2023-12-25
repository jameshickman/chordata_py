import json
from chordataweb.bin.html2nodes.converter import html_to_tag_builder
import time

"""
Support for metadata directives in the HTML files.

The directive is an HTML comment containing a JSON data packet of the following structure:
<!-- {
    "target": "python_file_to_write_to",
    "widgets": {
        "function_name": "Xpath/to/select/tag"
    }
} -->
"""


SOURCE = f"""from chordataweb.tagbuilder import TagBuilder
from chordataweb.util.translation import Translate


GENERATION_TIMESTAMP = {int(time.time())}


"""


class MetadataProcessor:
    def __init__(self, html: str):
        self.html_text = html
        self.config_block = {}
        self.has_metadata = False

    def find_config_block(self):
        start = self.html_text.find("<!-- {")
        if start == -1:
            return False
        end = self.html_text.find("} -->", start)
        if end == -1:
            return False
        json_text = self.html_text[start+5:end+1]
        try:
            self.config_block = json.loads(json_text)
        except json.decoder.JSONDecodeError:
            return False
        self.has_metadata = True
        return True

    def process_config_block(self):
        if not self.has_metadata:
            return False
        source = SOURCE
        for fctn_name in self.config_block['widgets']:
            search_path = self.config_block['widgets'][fctn_name]
            tag_text = html_to_tag_builder(self.html_text, search_path)
            if tag_text is not False:
                source += "def " + str(fctn_name) + "(t: Translate, includes: dict = None) -> TagBuilder:\n"
                source += "\t" + "return " + tag_text
                source += "\n\n"
        with open(self.config_block['target'] + ".py", 'w') as f:
            f.write(source)
