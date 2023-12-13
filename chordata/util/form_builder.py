from chordata.tagbuilder import TagBuilder
from chordata.util.translation import Translate


def form_builder(fields: list, translator: Translate):
    children = []
    for field in fields:
        if field.get('type') == 'text':
            children.append(text_input(field, translator))
        elif field.get('type') == 'number':
            children.append(number_input(field, translator))
        elif field.get('type') == 'textarea':
            children.append(text_area(field, translator))
        elif field.get('type') == 'select':
            children.append(select(field, translator))
        elif field.get('type') == 'checkbox':
            children.append(checkbox(field, translator))
        elif field.get('type') == 'trinary':
            children.append(trinary(field, translator))
        elif field.get('type') == 'address':
            children.append(address_fields(field, translator))
        elif field.get('type') == 'container':
            children.append(container(field, translator))
    return children


def build_input_attributes(field: dict, attribute_type: str) -> tuple:
    name = field.get('name', '')
    attributes = {'id': name, 'type': attribute_type, 'name': name}
    return name, attributes


def build_classes(field: dict, classes: list = None) -> str:
    if classes is None:
        classes = []
    if 'classes' in field:
        classes.extend(field['classes'])
    return " ".join(classes)


def build_label(field: dict, t: Translate) -> list:
    rv = [
        TagBuilder('span').add_attributes({'class': 'form__field-label'}).set_text(t.t(field.get('label')))
    ]
    if 'validation' in field:
        rv.append(
            TagBuilder('span').add_attributes({'class': 'form__field-required'}).set_text('*')
        )
    return rv


def text_input(field: dict, t: Translate) -> TagBuilder:
    name, attributes = build_input_attributes(field, 'text')
    return TagBuilder().add_attributes(
        {**{'class': build_classes(field, ['form__field-container'])}, **field.get('custom_attributes', {})}
    ).add_child(
        [
            TagBuilder('label').add_attributes({'for': name}).add_child(
                build_label(field, t)
            ),
            TagBuilder('input').add_attributes(attributes)
        ]
    ).add_data({'validation': field.get('validation', 'none')})


def number_input(field: dict, t: Translate) -> TagBuilder:
    name, attributes = build_input_attributes(field, 'number')
    return TagBuilder().add_attributes(
        {**{'class': build_classes(field, ['form__field-container'])}, **field.get('custom_attributes', {})}
    ).add_child(
        [
            TagBuilder('label').add_attributes({'for': name}).add_child(
                build_label(field, t)
            ),
            TagBuilder('input').add_attributes(attributes)
        ]
    ).add_data({'validation': field.get('validation', 'none')})


def text_area(field: dict, t: Translate) -> TagBuilder:
    name = field.get('name', '')
    return TagBuilder().add_attributes(
        {**{'class': build_classes(field, ['form__field-container'])}, **field.get('custom_attributes', {})}
    ).add_child(
        [
            TagBuilder('label').add_attributes({'for': name}).add_child(
                build_label(field, t)
            ),
            TagBuilder('textarea').add_attributes({'id': name, 'name': name})
        ]
    ).add_data({'validation': field.get('validation', 'none')})


def select(field: dict, t: Translate) -> TagBuilder:
    name = field.get('name', '')
    items = []
    for item in field.get('items', []):
        items.append(
            TagBuilder('option')
            .add_attributes({'value': item.get('field')})
            .set_text(t.t(item.get('label', '')))
        )
    return TagBuilder().add_attributes(
        {**{'class': build_classes(field, ['form__field-container'])}, **field.get('custom_attributes', {})}
    ).add_child(
        [
            TagBuilder('label').add_attributes({'for': name}).add_child(
                build_label(field, t)
            ),
            TagBuilder('select').add_attributes({'id': name, 'name': name}).add_child(items)
        ]
    ).add_data({'validation': field.get('validation', 'none')})


def checkbox(field: dict, t: Translate) -> TagBuilder:
    name = field.get('name', '')
    return TagBuilder().add_attributes(
        {**{'class': build_classes(field, ['form__field-container'])}, **field.get('custom_attributes', {})}
    ).add_child(
        [
            TagBuilder('input').add_attributes({'id': name, 'type': 'checkbox', 'name': name}),
            TagBuilder('label').add_attributes({'for': name}).add_child(
                build_label(field, t)
            )
        ]
    ).add_data({'validation': field.get('validation', 'none')})


def trinary(field: dict, t: Translate) -> TagBuilder:
    name = field.get('name', '')
    return TagBuilder().add_attributes(
        {
            **{'class': build_classes(field, ['form__field-container', 'form__field-container-trinary'])},
            **field.get('custom_attributes', {})
        }
    ).add_child(
        [
            TagBuilder('label').add_attributes({'for': name}).add_child(
                build_label(field, t)
            ),
            TagBuilder('select').add_attributes({'id': name, 'name': name}).add_child(
                [
                    TagBuilder('option').add_attributes({'value': ''}).set_text(t.t('None')),
                    TagBuilder('option').add_attributes({'value': 'yes'}).set_text((t.t('Yes'))),
                    TagBuilder('option').add_attributes({'value': 'no'}).set_text(t.t('No'))
                ]
            )
        ]
    ).add_data({'validation': field.get('validation', 'none')})


def address_fields(field: dict, t: Translate) -> TagBuilder:
    name = field.get('name', '')
    return TagBuilder().add_attributes(
        {
            **{'class': build_classes(field, ['form__field-container', 'form__field-map'])},
            **field.get('custom_attributes', {})
        }
    ).add_child([
        TagBuilder('label').set_text(t.t(field.get('title'))),
        TagBuilder().add_attributes({'class': 'form__field-map-container'}).add_child(
            [
                TagBuilder().add_attributes({'class': 'form__field-map-address'}).add_child(
                    [
                        TagBuilder('label').add_attributes({'for': name + '_address'}).set_text(t.t('Address')),
                        TagBuilder('input').add_attributes(
                            {'id': name + '_address', 'name': name + '_address', 'type': 'text'}
                        )
                    ]
                ),
                TagBuilder().add_attributes({'class': 'form__field-map-city'}).add_child(
                    [
                        TagBuilder('label').add_attributes({'for': name + '_city'}).set_text(t.t('City')),
                        TagBuilder('input').add_attributes(
                            {'id': name + '_city', 'name': name + '_city', 'type': 'text'}
                        )
                    ]
                ),
                TagBuilder().add_attributes({'class': 'form__field-map-state'}).add_child(
                    [
                        TagBuilder('label').add_attributes({'for': name + '_city'}).set_text(t.t('State')),
                        TagBuilder('input').add_attributes(
                            {'id': name + '_city', 'name': name + '_city', 'type': 'text'}
                        )
                    ]
                ),
                TagBuilder().add_attributes({'class': 'form__field-map-zip'}).add_child(
                    [
                        TagBuilder('label').add_attributes({'for': name + '_zip'}).set_text(t.t('ZIP/Post code')),
                        TagBuilder('input').add_attributes(
                            {'id': name + '_zip', 'name': name + '_zip', 'type': 'text'}
                        )
                    ]
                )
            ]
        )
    ]).add_data(
        {
            'validation': field.get('validation', 'required'),
            'show_map': field.get('map', 'no')
        }
    )


def container(field: dict, t: Translate) -> TagBuilder:
    section = TagBuilder(field.get('tag', 'div')).add_attributes(
        {
            **{'class': build_classes(field, ['form__field-container', 'form__field-section'])},
            **field.get('custom_attributes', {})
        }
    ).add_child(form_builder(field.get('children', []), t))
    if 'data' in field:
        section.add_data(field['data'])
    return section
