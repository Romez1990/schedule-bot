from typing import (
    Iterable,
    Mapping,
)


def repr_list(elements: Iterable[object]) -> str:
    elements_repr = map(indent_multiline, elements)
    joined_elements = ',\n'.join(elements_repr) + ','
    return f'[\n{joined_elements}\n]'


def repr_dict(mapping: Mapping[object, object]) -> str:
    mapping_repr = map(indent_pair_multiline, mapping.items())
    joined_pairs = ',\n'.join(mapping_repr) + ','
    return f'{{\n{joined_pairs}\n}}'


def indent_multiline(value: object) -> str:
    lines = repr(value).split('\n')
    indented_lines = map(indent_line, lines)
    return '\n'.join(indented_lines)


def indent_pair_multiline(pair: tuple[object, object]) -> str:
    key, value = pair
    lines = repr(value).split('\n')
    lines[0] = f'{repr(key)}: ' + lines[0]
    indented_lines = map(indent_line, lines)
    return '\n'.join(indented_lines)


def indent_line(line: str) -> str:
    return ' ' * 4 + line
