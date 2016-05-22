class Plugin(object):
  def get_command_line_options(self):
    return []

  def process_command_line_options(self, test_driver, **options):
    pass

  def init(self, test_driver):
    pass

  def start_running_test(self, test_driver, klass, method_name):
    pass

  def start_running_test_try(self, test_driver, klass, method_name):
    pass

  def finish_running_test_try(self, test_driver, klass, method_name):
    pass

  def test_success(self, test_driver, klass, method_name):
    pass

  def test_failure(self, test_driver, klass, method_name, ex, st):
    pass

  def post_test_checks(self, test_driver, klass, method):
    pass

  def finish_running_tests(self, test_driver):
    pass


