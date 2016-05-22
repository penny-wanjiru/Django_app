from django_test.plugins import Plugin
from coverage import coverage

class CoveragePlugin(Plugin):
  def init(self, test_driver):
    self.coverage = coverage()

  def start_running_test_try(self, test_driver, klass, method_name):
    self.coverage.start()

  def finish_running_test_try(self, test_driver, klass, method_name):
    self.coverage.stop()

  def finish_running_tests(self, test_driver):
    try:
      self.coverage.html_report(directory = 'covhtml')
    except:
      pass #HACK

