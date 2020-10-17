from os import environ, system
from sys import argv
from pathlib import Path

project_root = Path(__file__).parent.parent
environ['PYTHONPATH'] = str(project_root.absolute())

module_path = Path(argv[1])
system(f'python {module_path}')
