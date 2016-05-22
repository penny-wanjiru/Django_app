from django.core.management.base import BaseCommand
from optparse import make_option
from django_test import CustomTestRunner, command_line_options


class Command(BaseCommand):
  option_list = list(BaseCommand.option_list) + \
                [make_option(*o.args, **o.kwargs) for o in command_line_options]


  def handle(self, *args, **options):
    try:
      from south.management.commands import patch_for_test_db_setup
      patch_for_test_db_setup()
    except ImportError:
      pass

    CustomTestRunner().run_tests(*args, **options)

