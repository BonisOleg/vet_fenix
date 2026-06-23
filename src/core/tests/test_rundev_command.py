from django.core.management import get_commands
from django.test import SimpleTestCase


class RundevCommandTests(SimpleTestCase):
    def test_rundev_command_is_registered(self) -> None:
        self.assertIn('rundev', get_commands())
