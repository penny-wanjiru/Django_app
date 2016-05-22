from django_test.plugins import Plugin
from django_test import OptionDescriptor

class HudsonPlugin(Plugin):
  def get_command_line_options(self):
    return [OptionDescriptor("-f", "--failed", dest = "failed", action = "store")]

  def process_command_line_options(self, test_driver, **options):
    if options.get("failed", None):
      from playfi.util.hudson import get_failed_test_names
      for p in get_failed_test_names(int(options["failed"])):
        test_driver.add_path(p)
      return True



