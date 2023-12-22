import xml.etree.ElementTree as ET


def html_to_tag_builder(html_string: str, starting_node: str = None) -> (str, bool):
    def parse(node: ET) -> str:
        code = "TagBuilder("
        if node.tag.lower() != 'div':
            code += "\"" + node.tag.lower() + "\""
        code += ")"
        if len(node.attrib.keys()) > 0:
            code += ".add_attributes(" + str(node.attrib) + ")"
        if node.text and len(node.text.strip()) > 0:
            s = node.text.strip()
            if s[0] == "$" or s[0] == "{":
                code += ".set_text(\"" + s + "\")"
            else:
                code += ".set_text(t.t(\"" + node.text.strip() + "\"))"
        if len(node) > 0:
            code_children = []
            for child in node:
                code_children.append(parse(child))
            code += ".add_child([\n" + ",\n ".join(code_children) + "])"
        return code

    root = ET.fromstring(html_string)
    if starting_node is not None:
        root = root.find(starting_node)
        if root is None:
            return False
    return parse(root)

