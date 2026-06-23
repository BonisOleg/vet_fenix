import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

base_dir = Path(__file__).resolve().parent.parent
src_path = base_dir / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_asgi_application()
