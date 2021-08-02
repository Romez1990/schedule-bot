from sys import path, argv
from importlib import import_module
from pathlib import Path

project_root = Path(__file__).parent.parent
source_root = project_root / 'src'
path.append(str(source_root))

script_name = argv[1]
try:
    import_module(script_name)
except KeyboardInterrupt:
    pass
