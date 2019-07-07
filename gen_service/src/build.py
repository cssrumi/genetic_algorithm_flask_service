import os

if os.getenv('ENV', 'DEV').upper() == 'DEV':
    python = '..\\..\\venv\\Scripts\\python' if os.name == 'nt' else '../../venv/bin/python'
else:
    python = 'python'
os.system(f'{python} setup.py build_ext --inplace')
os._exit(0)
