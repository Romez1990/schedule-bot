from sys import argv, exit
from importlib import import_module

if len(argv) != 2:
    raise ValueError('must be 2 arguments')

script_name = argv[1]
script_name = script_name.replace('-', '_')

try:
    import_module(f'scripts.{script_name}')
except ModuleNotFoundError as err:
    print(err)
    exit(1)
