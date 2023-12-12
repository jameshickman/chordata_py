import json
from chordata.tagbuilder import TagBuilder


def boot_webbus_components(components: list, page_vars: [dict, None] = None) -> TagBuilder:
    lines = []
    for component in components:
        for n in component:
            lines.append(
                "'" + n + "': " + component[n]
            )
    component_set = ",\n".join(lines)
    if isinstance(page_vars, dict):
        page_set = json.dumps(page_vars)
        script = f"""
        window.addEventListener('load', () => {{
            new WebBus(
                {{
                    "prototypes": {{ {component_set} }},
                    "page": {page_set}
                }}
            );
        }});
        """
    else:
        script = f"""
        window.addEventListener('load', () => {{
            new WebBus(
                {{
                    "factories": {{ {component_set} }}
                }}
            );
        }});
        """
    return TagBuilder('script').set_text(script)
