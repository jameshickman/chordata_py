#!/usr/bin/env python3


"""
Chordata command line project creation tool
"""

import os
import sys
from string import Template


wd = os.getcwd()


def create_project():
    app_dir = os.path.join(wd, "apps")
    os.mkdir(app_dir)
    init_filename = os.path.join(app_dir, "__init__.py")
    with open(init_filename, "w") as f:
        f.write("# Chordata Apps package\n")
    static_dir = os.path.join(wd, "static")
    os.mkdir(static_dir)
    static_global_dir = os.path.join(static_dir, "_global")
    os.mkdir(static_global_dir)
    print("Default Chordata Apps package and static files directory created.\n")
    return


def create_app(app_name: str):
    app_dir = os.path.join(wd, "apps", app_name)
    app_init = os.path.join(app_dir, "__init__.py")
    app_static_dir = os.path.join(app_dir, "static")
    app_template_dir = os.path.join(app_dir, "templates")
    app_main_file = os.path.join(app_dir, "main.py")
    app_routes_file = os.path.join(app_dir, "routes.json")
    app_template_file = os.path.join(app_template_dir, "index.html")
    os.mkdir(app_dir)
    os.mkdir(app_static_dir)
    os.mkdir(app_template_dir)
    with open(app_init, "w") as f:
        f.write("# Chordata App: " + str(app_name) + "\n")
    with open(app_template_file, "w") as f:
        f.write(BOILERPLATE_TEMPLATE)
    with open(app_routes_file, "w") as f:
        f.write(BOILERPLATE_ROUTES)
    main_py_text = Template(BOILERPLATE_MAIN_PY).substitute(app_name=app_name)
    with open(app_main_file, "w") as f:
        f.write(main_py_text)
    print("Successfully created App named: " + str(app_name) + ".")
    return


def html2code(html_file: str, start_node: str = None):
    if not os.path.exists(html_file):
        print(ERR_MISSING_FILE)
    from chordataweb.bin.html2nodes.converter import html_to_tag_builder
    from chordataweb.bin.html2nodes.metadata import MetadataProcessor
    with open(html_file, "r") as f:
        html = f.read()
    processor = MetadataProcessor(html)
    if start_node is None and processor.find_config_block():
        print(MSG_PROCESSING_DIRECTIVES)
        processor.process_config_block()
    else:
        code = html_to_tag_builder(html, start_node)
        if code is False:
            print(ERR_INVALID_SEARCH)
        else:
            print(code)
        return


BOILERPLATE_ROUTES = """{
    "index": {
        "package": "main",
        "function": "index",
        "permissions": {
            "get": [],
            "post": [],
            "delete": [],
            "default": []
        }
    }
}
"""


BOILERPLATE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>New App</title>
</head>
<body>
    <h1>New App named: {{app_name}}</h1>
</body>
</html>
"""


BOILERPLATE_MAIN_PY = """from chordataweb.server_env import ServerEnvironment


def index(e: ServerEnvironment, s: dict):
    rv = {
        "app_name": "${app_name}" 
    }
    return rv, {'template': 'index.html', 'type': 'text/html'}

"""


HELP = """
Available operations:
    init - create default Chordate directory structure for Apps and default static files.
    create <app_name> - Create a new Chordate App structure in the local Apps Directory.
                        If the HTML file contains a metadata object encoded as a JSON object,
                        it will write a Python source file with functions as defined in the metadata object.
    html2code <html_file> <base_node: optional> - Convert an HTML file to equivalent Python code using TagBuilder
                                                  Code is written to stdout, so pipe into a file. The optional
                                                  third parameter can be an Xpath to the tag to start conversion at.
"""

MSG_PROCESSING_DIRECTIVES = "Directives block found in template. Generating source file..."

ERR_MISSING_APP_NAME = "You need to pass a name for your new Chordata App."

ERR_MISSING_HTML_FILE = "You need to specify an HTML file."

ERR_MISSING_FILE = "Cannot find the file!"

ERR_INVALID_SEARCH = "The XPath search did match any tag in the HTML file."


def main():
    arguments = sys.argv[1:]
    if len(arguments) == 0 or arguments[0] == "help":
        print(HELP)
    elif arguments[0] == "init":
        create_project()
    elif arguments[0] == "create":
        if len(arguments) < 2:
            print(ERR_MISSING_APP_NAME)
        else:
            create_app(arguments[1])
    elif arguments[0] == "html2code":
        if len(arguments) < 2:
            print(ERR_MISSING_HTML_FILE)
        else:
            if len(arguments) == 3:
                html2code(arguments[1], arguments[2])
            else:
                html2code(arguments[1])


if __name__ == "__main__":
    main()
