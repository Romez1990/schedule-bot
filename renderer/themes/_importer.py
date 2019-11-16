from pathlib import Path
from importlib import import_module
from typing import Dict

from ._theme import Theme


def import_themes() -> Dict[str, Theme]:
    themes: Dict[str, Theme] = {}
    directory = Path(__file__).parent
    for file in directory.iterdir():
        if file.is_dir() or file.name.startswith('_'):
            continue
        module_name: str = file.stem
        current_package_name = '.'.join(__name__.split('.')[:-1])
        module = import_module(f'{current_package_name}.{module_name}')
        themes[file.stem] = getattr(module, f'{module_name.capitalize()}Theme')
    return themes
