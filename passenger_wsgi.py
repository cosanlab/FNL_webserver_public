#c/v from luke; will likely need to be modified slightly

import sys, os

INTERP = os.path.join(os.environ['HOME'], '/home/cosanlab/venv', 'bin', 'python')

if sys.executable !=INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app import app as application
