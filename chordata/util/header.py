from chordata.tagbuilder import TagBuilder


def build_head_tag(
        title: str,
        css_files: list = None,
        javascript_files: list = None,
        head_classes: list = None) -> TagBuilder:
    head_tags = []
    if isinstance(css_files, list):
        css_files = list(set(css_files))
        for file in css_files:
            head_tags.append(
                TagBuilder('link').add_attributes({'rel': 'stylesheet', 'href': file})
            )
    if isinstance(javascript_files, list):
        jsf = []
        scripts = []
        for s in javascript_files:
            if not s['src'] in scripts:
                scripts.append(s['src'])
                jsf.append(s)
        for script in jsf:
            attr = {'src': script.get('src')}
            if 'type' in script:
                attr['type'] = script.get('type')
            head_tags.append(
                TagBuilder('script').add_attributes(attr)
            )
    head = TagBuilder('head').add_child(
                TagBuilder('title').set_text(title)
            ).add_child(head_tags)
    if isinstance(head_classes, list):
        head.add_attributes({'classes': ' '.join(head_classes)})
    return head
