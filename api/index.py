import os
import sys

# Ensure Matplotlib uses writable /tmp directory on serverless runtimes
os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')

# Ensure project root is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app
