"""
This is a vastly improved test runner over django's in-built runner.

Features:

  - Exceptions and failures are reported instantly, and you're
    given the option to launch a debugger at the point of failure.
  - Pretty printing of stack traces -- frames involving your own
    code are highlighted.
  - Assert statements produce prettified output.
  - Integrated selenium support:
    - The test runner transparently starts its own self-contained (CherryPy)
      server that the selenium tests access.
    - We have a "--max-tries" argument that you can use to retry failed tests,
      since selenium tests can be fragile and rely on timing.
  - Support for separate workers if you want to run tests in parallel;
    vastly improves test suite run times for selenium tests.
  - Can run tests by partial paths rather than full paths (eg. can specify
    just the test _method_ name from the command line, rather than the
    full module path).
  - Test tagging.
  - Coverage integration.
  - Produces XML reports of 
  - Some hudson integration: can choose to run all the tests that failed 
    in a particular build.
  - Support for "variations" on tests: a way to slightly change tests
    with a minimum of code.


Usage:
  - Add 'django_test' to your settings.INSTALLED_APPS
    - This will replace the `manage.py test` command with `django_test`'s,
      which is mostly compatible with django's but has many improvements.

  - Make your test classes derive from django_test.TestCase (or django_test.selenium.SeleniumTestCase)

  - Run python manage.py test as normal:

    eg:
      python manage.py test module1.module2.module3
      python manage.py test module1.module2.Class
      python manage.py test module1.module2.Class.method

  - Settings in settings.TEST_SETTINGS dictionary will override normal settings
  - To run Selenium tests, set RUN_SELENIUM_TESTS to True

TODO:
  - Currently, only classes ending with "Test" and methods
    starting with "test_" are found when looking for tests.
  - We don't have the full set of assert* functions.
  - We don't trap stdout output, so print statements in the
    tests will get in the way of the test results.  Would
    be better to save this somewhere and control when 
    we output it.
"""

import sys
import shutil
import itertools
import pprint
import inspect
import traceback, re, os, pdb      
from django import db
from django.core import mail
from django.conf import settings
from django.db import connection, transaction
from django.test.testcases import disable_transaction_methods, restore_transaction_methods
from django.core.urlresolvers import clear_url_caches
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from django.db import connections, DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.test.utils import setup_test_environment, teardown_test_environment

from django_test.utils import import_object, import_module, restore_database
from django_test.variations import MyVariationRunner


class OptionDescriptor(object):
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs


PLUGINS = [import_object(path)() for path in settings.TEST_PLUGINS]

command_line_options = [
  OptionDescriptor("-s", "--noselenium", dest = "no_selenium", action = "store_true"),
  OptionDescriptor("-l", "--long", dest = "run_long_tests", action = "store_true"),
  OptionDescriptor("-g", "--grep", dest = "grep", action = "append"),
  OptionDescriptor("-t", "--tag", dest = "tag", action = "store"),
  OptionDescriptor("-m", "--max-tries", dest = "max_tries", action = "store", 
                         type = "int", default = 1),
  OptionDescriptor("-n", "--never-debug", dest = "never_debug", action = "store_true", 
                         default = False),
  #TODO:
  #make_option('--numworkers', '-n', dest='num_workers',
  #    help='The number of workers.'),
  #make_option('--workernum', '-w', dest='worker_num',
  #    help='The number of this worker [0..numworkers-1].'),
]

for p in PLUGINS:
  command_line_options.extend(p.get_command_line_options())
  

def for_all_plugins(method_name, *args, **kwargs):
  for p in PLUGINS:
    getattr(p, method_name)(*args, **kwargs)



class Filter(object):
  def test_class(self, klass):
    return True

  def test_method(self, klass, method):
    return True


class GrepFilter(Filter):
  def __init__(self, string):
    self.string = string

  def test_class(self, klass):
    return any((self.string in get_method_path(klass, n) \
                for n in dir(klass) \
                if n.startswith("test_")))

  def test_method(self, klass, method):
    return self.string in get_method_path(klass, method)


class TagFilter(Filter):
  def __init__(self, tag):
    self.tag = tag

  def test_class(self, klass):
    return any((self.tag in getattr(getattr(klass, n, None), 'tags', [])
                for n in dir(klass) \
                if n.startswith("test_")))

  def test_method(self, klass, method):
    return self.tag in getattr(method, 'tags', [])


class NoSeleniumFilter(Filter):
  def test_class(self, klass):
    return not getattr(klass, 'selenium_test', False)


class NoLongTestsFilter(Filter):
  def test_method(self, klass, method):
    return not getattr(method, "long_test", False)


def get_method_path(klass, method):
  if hasattr(method, "__name__"):
    method = method.__name__

  return "%s.%s.%s" % (klass.__module__, klass.__name__, method)



class TestDriver(object):
  def __init__(self, 
               test_paths = None, 
               num_workers = None, 
               worker_num = None,
               max_tries = 1,
               never_debug = False):
    self.test_paths = test_paths
    self.num_workers = num_workers \
                       if num_workers != None \
                       else getattr(settings, "NUM_WORKERS", 1)
    self.worker_num = worker_num \
                      if worker_num != None \
                      else getattr(settings, "WORKER_NUM", 0)
    self.verbosity = 1
    self.max_tries = max_tries
    self.never_debug = never_debug

    self.passed = 0
    self.errors = 0
    self.tests_seen = 0
    self.tests_run = 0

    for_all_plugins("init", self)

    self.modules = []
    self.classes = []
    self.methods = []

    self.filters = []  # List of Filter objects


  def add_path(self, path):
    obj = import_object(path.replace(":", "."))

    if inspect.ismodule(obj):
      self.add_module(obj)
    elif inspect.isclass(obj):
      self.add_class(obj)
    elif inspect.ismethod(obj):
      self.add_method(obj.im_class, obj.__name__)
    else:
      raise Exception("%s should be a module, class or method." % self.test_path)


  def add_all_tests(self):
    modules = []
    for a in settings.INSTALLED_APPS:
      try:
        module = import_module(a + ".tests")
        if module not in modules:
          modules.append(module)
      except ImportError:
        print "Could not import %s" % (a + ".tests")

    for m in modules:
      self.add_module(m)


  def run(self):
    setup_test_environment()
    settings.DEBUG = False
    old_name = settings.DATABASES["default"]["NAME"]
    
    if hasattr(settings, "TEST_SETTINGS"):
      for k, v in settings.TEST_SETTINGS.iteritems():
        setattr(settings, k, v)

    connection.creation.create_test_db(self.verbosity, 
                                       autoclobber = True)

    db.connections["default"].close()
    db_name = settings.DATABASES["default"]["TEST_NAME"]
    shutil.copyfile(db_name, db_name + ".bak")
    
    self.run_tests()

    connection.creation.destroy_test_db(old_name, self.verbosity)
    teardown_test_environment()

    print "%s passed, %s failed" % (self.passed, self.errors)


  def add_module(self, module):
    self.modules.append(module)

  def add_class(self, klass):
    self.classes.append(klass)

  def add_method(self, klass, method_name):
    self.methods.append((klass, method_name))

  def test_method(self, class_or_object, method_name):
    if inspect.isclass(class_or_object):
      klass = class_or_object
      ob = class_or_object()
    else:
      klass = class_or_object.__class__
      ob = class_or_object

    method = ob.__getattribute__(method_name)
    method_path = "%s.%s.%s" % (klass.__module__, klass.__name__, method_name)

    self.tests_seen += 1

    if self.tests_seen % self.num_workers != self.worker_num:
      return

    if self.filters and any((not p.test_method(klass, method) for p in self.filters)):
      return

    print >>sys.stderr, "-" * 50
    print >>sys.stderr, "%s (Worker %s/%s)" % \
          (method_path, self.worker_num, self.num_workers)
    print >>sys.stderr, "-" * 50

    try_num = 1
    finished = False
    torn_down = False

    for_all_plugins("start_running_test", self, klass, method_name)

    while not finished and try_num <= self.max_tries:
      try:
        # Actually run the test
        if getattr(method, "is_operation_test", False):
          for_all_plugins("start_running_test_try", self, klass, method_name)
          method()
          for_all_plugins("finish_running_test_try", self, klass, method_name)
          torn_down = True
        elif getattr(method, "has_variations", False):
          for_all_plugins("start_running_test_try", self, klass, method_name)
          MyVariationRunner().run_test(method)
          for_all_plugins("finish_running_test_try", self, klass, method_name)
          torn_down = True
        else:
          ob._test_setup()
          ob.setUp()
          for_all_plugins("start_running_test_try", self, klass, method_name)
          method()
          for_all_plugins("finish_running_test_try", self, klass, method_name)

        for_all_plugins("post_test_checks", self, klass, method)
        for_all_plugins("test_success", self, klass, method)
        finished = True

        print >>sys.stderr, "PASSED"
        self.passed += 1
        self.tests_run += 1
      except Exception, e:
        for_all_plugins("finish_running_test_try", self, klass, method_name)

        if try_num == self.max_tries:
          etype, value, tb = sys.exc_info()
          
          st = traceback.format_tb(tb)
          ex = traceback.format_exception_only(etype, value)
          
          for_all_plugins("test_failure", self, klass, method_name, ex, st)
          
          for line in itertools.chain(st, ex):
            print >>sys.stderr, re.sub('(' + os.getcwd() + ')(.*)", (line \\d+)', 
                         '\\1\033[1;31m\\2\033[0;0;0m", \033[1;32m\\3\033[0;0;0m', 
                         line)

          if not self.never_debug:
            print "Would you like to debug? [y/N/neVer]"
            c = raw_input()
            if c.lower() == "y":
              pdb.post_mortem(sys.exc_info()[2])
            if c.lower() == "v":
              self.never_debug = True

          self.errors += 1
          self.tests_run += 1
        else:
          print "Failed.. retrying"

        try_num += 1
      finally:
        if not torn_down:
          ob.tearDown()
          ob._test_teardown()


  def test_class(self, klass):
    """
    We only create one instance of the test class, so consumers can
    put test-case-level initialisation in the class's __init__ method.
    """

    instance = klass()  

    for class_member_name in klass.__dict__:
      class_member = getattr(klass, class_member_name)
      if inspect.ismethod(class_member) and class_member_name.startswith("test_"):
        self.test_method(instance, class_member_name)

    if getattr(instance, "post_last_teardown", None):
      instance.post_last_teardown()


  def test_module(self, module):
    for module_object_name in dir(module):
      module_object = getattr(module, module_object_name)
      if inspect.isclass(module_object):
        klass = module_object
        if issubclass(klass, TestCase):
          if self.filters and any((not f.test_class(klass) for f in self.filters)):
            continue
          self.test_class(klass)


  def run_tests(self):
    for m in self.modules:
      self.test_module(m)

    for c in self.classes:
      self.test_class(c)

    for c, m in self.methods:
      instance = c()
      self.test_method(instance, m)
      if getattr(instance, "post_last_teardown", None):
        instance.post_last_teardown()

    for_all_plugins("finish_running_tests", self)


class CustomTestRunner(object):
  def run_tests(self, *test_paths, **options):
    driver = TestDriver(max_tries = options['max_tries'])

    driver.never_debug = options["never_debug"]

    if not test_paths and not options["grep"] and not options["run_long_tests"]:
      driver.filters.append(NoLongTestsFilter())
    if options['no_selenium']:
      driver.filters.append(NoSeleniumFilter())

    if test_paths:
      for p in test_paths:
        driver.add_path(p)
    elif options['grep']:
      driver.add_all_tests()
      for g in options['grep']:
        driver.filters.append(GrepFilter(g))
    elif options['tag']:
      driver.add_all_tests()
      driver.filters.append(GrepFilter(options['tag']))
    else:
      add_all_tests = True
      for p in PLUGINS:
        handled = p.process_command_line_options(driver, **options)
        if handled:
          add_all_tests = False
          break
      if add_all_tests:
        driver.add_all_tests()

      
    driver.run()



class TestCase(object):
  def __init__(self):
    pass

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def assertEqual(self, o1, o2, message = ""):
    if isinstance(o1, QuerySet) or isinstance(o2, QuerySet):
      # Allow comparing of two `QuerySet`s, or a `QuerySet` and a `list`,
      # by converting `QuerySet`s to `list`s.
      return self.assertEqual(list(o1) if isinstance(o1, QuerySet) else o1,
                              list(o2) if isinstance(o2, QuerySet) else o2,
                              message)

    if o1 != o2:
      raise Exception("Not equal: \n%s\nand\n%s" % (pprint.pformat(o1)[0:10000],
                                                    pprint.pformat(o2)[0:10000])
                      + message)

  def assertContains(self, o1, o2, message = ""):
    if o2 not in o1:
      raise Exception("Not contained: \n%s\nand\n%s" % (pprint.pformat(o1)[0:10000],
                                                        pprint.pformat(o2)[0:10000])
                      + message)

  def assertTrue(self, o1):
    if not o1:
      raise Exception("Not true")

  def assertFalse(self, o1):
    if o1:
      raise Exception("Not false")

  def assertRaises(self, exc_type, func):
    try:
      func()
    except exc_type as ex:
      pass
    except Exception as ex:
      raise Exception("%s exception raised - we expected %s" % (ex, exc_type))
    else:
      raise Exception("No exception raised - we expected %s" % exc_type)

  def assertColumnsEqual(self, *args):
    for left, right in args:
      self.assertEqual(left, right)

  def _setup_urlconf(self):
    if hasattr(self, 'urls'):
      self._old_root_urlconf = settings.ROOT_URLCONF
      settings.ROOT_URLCONF = self.urls
      clear_url_caches()

  def _teardown_urlconf(self):
    if hasattr(self, '_old_root_urlconf'):
      settings.ROOT_URLCONF = self._old_root_urlconf
      clear_url_caches()

  def _flush_databases(self):
    # If the test case has a multi_db=True flag, flush all databases.
    # Otherwise, just flush default.
    if getattr(self, 'multi_db', False):
      databases = connections
    else:
      databases = [DEFAULT_DB_ALIAS]

    for db in databases:
      call_command('flush', verbosity=0, interactive=False, database=db)


  def setup_database(self, transactions = True):
    if not transactions:
      transaction.enter_transaction_management()
      transaction.managed(True)
      disable_transaction_methods()
    else:
      restore_database()

    Site.objects.clear_cache()

    if hasattr(self, 'fixtures'):
      call_command('loaddata', *self.fixtures, **{
                                                   'verbosity': 0,
                                                   'commit': False
                                                 })

  def teardown_database(self, transactions = True):
    if not transactions:
      try:
        restore_transaction_methods()
      except:
        pass
      try:
        transaction.rollback()
      except:
        pass
      try:
        transaction.leave_transaction_management()
      except:
        pass


  def _test_setup(self):
    """
    From django.test.testcases.TestCase._fixture_setup
    """

    self._setup_urlconf()
    self.setup_database(transactions = False)

  def _test_teardown(self):
    """
    From django.test.testcases.TestCase._fixture_teardown
    """
    mail.outbox = []
    self.teardown_database(transactions = False)
    self._teardown_urlconf()





