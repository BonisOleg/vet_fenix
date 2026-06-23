#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    src_path = base_dir / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.develop'),
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Install dependencies from requirements.txt."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
