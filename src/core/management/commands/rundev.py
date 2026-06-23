"""Stable local development server with autoreload disabled by default."""

from __future__ import annotations

import sys

from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)


class Command(RunserverCommand):
    help = (
        'Start a stable development server. Autoreload is off by default '
        'so IDE and tooling file changes do not stop the server.'
    )

    def add_arguments(self, parser) -> None:
        super().add_arguments(parser)
        parser.add_argument(
            '--reload',
            action='store_true',
            help='Enable autoreload when Python files change.',
        )

    def handle(self, *args, **options) -> None:
        if '--reload' in sys.argv:
            options['use_reloader'] = True
        elif '--noreload' in sys.argv:
            options['use_reloader'] = False
        else:
            options['use_reloader'] = False
        super().handle(*args, **options)
