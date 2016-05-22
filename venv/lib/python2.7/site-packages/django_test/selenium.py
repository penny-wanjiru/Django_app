import sys
import os
import re
from django.utils import simplejson
from time import sleep
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler
from cherrypy.wsgiserver import CherryPyWSGIServer
from threading import Thread
from django.conf import settings
from selenium_python import selenium #TODO
from sxml.parser import expression as jquery_expression

import socket
import logging

from django_test import TestCase
from django_test.utils import restore_database

# We still have the pip "selenium" package renamed to seleniumzzz
# to avoid naming conflicts.  TODO.
from seleniumzzz import webdriver
from seleniumzzz.webdriver.support.wait import WebDriverWait
from seleniumzzz.webdriver.common.action_chains import ActionChains
from seleniumzzz.webdriver.support.select import Select


class ConvenientSelenium(webdriver.Firefox):
  def __init__(self, *args, **kwargs):
    super(ConvenientSelenium, self).__init__(*args, **kwargs)


  def get_location(self):
    """
    For backwards compatibility.
    """
    return self.current_url


  def wait_for_page_to_load(self, timeout = 5000):
    """
    Backwards compatibility?  Don't know what to do as there is no replacement.
    """
    pass


  def wait_for_condition(self, condition, timeout = 5000):
    js = condition
    WebDriverWait(self, timeout / 1000).until(lambda x: self.execute_javascript(js))
      


  def open(self, location):
    # This will remove some insidious errors that can occur in the following situation:
    # - Test 1 leaves the browser in a location with a hash (eg. http://localhost:8000/blah#hash)
    # - Test 2 starts by trying to open the same url and hash (http://localhost:8000/blah#hash)
    # - In this case, in test 2, the browser would not make any request at all, since it
    #   thinks there is just a hash change.  Therefore the open() call will timeout.
    # So if the old and new urls are the same, we load a blank url, to make sure they aren't.

    def get_up_to_hash(s):
      a = self.get_absolute_location(s)
      return a[0:a.index("#")] if "#" in a else a

    print >>sys.stderr, "going for ", self.get_absolute_location(location)
    num_tries = 0
    while True:
      try:
        super(ConvenientSelenium, self).get(self.get_absolute_location(location))
        break
      except Exception, e:
        if num_tries > 10:
          raise

        num_tries += 1
        sleep(2)


  def execute_javascript(self, js_string, parse_json = False):
    if parse_json:
      result = self.execute_script("var env = window; return env.$.toJson(%s)" % js_string)
      return simplejson.loads(result)
    else:
      return self.execute_script("var env = window; return " + js_string.strip())


  def get_absolute_location(self, location):
    return location \
           if location.startswith("http://") \
           else "http://localhost:%s%s" % (settings.CHERRYPY_PORT, location)


  def resolve_locator(self, locator):
    """
    We support (some) jQuery locators now!  We treat a locator as a jQuery locator
    if it doesn't start with a forward slash (ie. is not XPath), and is not a 
    valid ID for a DOM object.  
    """
    if not locator.startswith("/"):
      # Use sxml's parser to convert the jQuery selector to an XPath string.
      return jquery_expression.parse(locator)[0].to_xpath()
    else:
      return locator


  def _wait_if_asked(self, locator, wait):
    if wait:
      self.wait_for_condition("""env.$ != null && env.$("%s").length > 0""" % locator)

  def get_text(self, locator, wait = False):
    self._wait_if_asked(locator, wait)
    return self.find_element_by_xpath(self.resolve_locator(locator)).text

  def click(self, locator, wait = True):
    """
    If wait == True, we use jQuery on the locator to wait for 
    at least one matching element to exist before trying to click.
    """
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).click()

  def mouse_over(self, locator, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).mouse_over()

  def mouse_down(self, locator, wait = False):
    self._wait_if_asked(locator, wait)
    a = ActionChains(self)
    a.click_and_hold(self.find_element_by_xpath(self.resolve_locator(locator)))
    a.perform()

  def mouse_up(self, locator, wait = False):
    self._wait_if_asked(locator, wait)
    a = ActionChains(self)
    a.release(self.find_element_by_xpath(self.resolve_locator(locator)))
    a.perform()

  def mouse_down_at(self, locator, position, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).mouse_down_at(position)

  def mouse_move_at(self, locator, position, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).mouse_move_at(position)

  def mouse_up_at(self, locator, position, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).mouse_up_at(position)

  def type(self, locator, text, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).send_keys(text)

  def drag_and_drop(self, locator, movements_string, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).drag_and_drop(movements_string)

  def fire_event(self, locator, event_name, wait = False):
    self._wait_if_asked(locator, wait)
    self.find_element_by_xpath(self.resolve_locator(locator)).fire_event(event_name)

  def select(self, select_locator, 
             value = None, label = None, id = None, index = None, 
             wait = False):

    self._wait_if_asked(select_locator, wait)

    el = self.find_element_by_xpath(self.resolve_locator(select_locator))
    select = Select(el)
    if value != None:
      select.select_by_value(value)
    elif label != None:
      select.select_by_visible_text(label)
    elif id != None:
      select.select_by_id(id)
    elif index != None:
      select.select_by_index(index)

  def get_selected_value(self, locator, wait = False):
    self._wait_if_asked(locator, wait)
    return self.find_element_by_xpath(self.resolve_locator(locator)).selected_value

  def get_value(self, locator, wait = False):
    self._wait_if_asked(locator, wait)
    return self.find_element_by_xpath(self.resolve_locator(locator)).value

  def drag_and_drop_to_object(self, locator_from, locator_to, wait = False):
    self._wait_if_asked(locator_from, wait)
    self._wait_if_asked(locator_to, wait)
    super(ConvenientSelenium, self).drag_and_drop_to_object(
      self.resolve_locator(locator_from),
      self.resolve_locator(locator_to),
    )


  def get_element_position_top(self, locator, wait = False):
    """
    Contrary to selenium.get_element_position_top, returns an integer.
    """
    self._wait_if_asked(locator, wait)
    l = self.resolve_locator(locator)
    str = super(ConvenientSelenium, self).get_element_position_top(l)
    return int(str)

  def get_combo_box_options(self, selector):
    str = \
      """
      env.toJson(env.$.map(env.$("%s").find("option"), 
                           function(e) { 
                             return [[env.$(e).val(), 
                                      env.$(e).html()]]; 
                           }))
      """ % selector

    out = self.execute_javascript(str)
    return simplejson.loads(out)



class SeleniumTestCase(TestCase):
  """
  TestCase subclass that starts a selenium instance *and a web server*.
  The selenium instance is accessible to subclasses as ``self.selenium``.

  Manages the database like a django TransactionTestCase, since the general use
  case is to be calling views that manage their own transactions.
  """
  selenium_test = True

  def __init__(self):
    super(SeleniumTestCase, self).__init__()
    self.backup_settings = {}

    for k, v in self.get_selenium_settings().iteritems():
      self.backup_settings[k] = getattr(settings, k)
      setattr(settings, k, v)




  def __getattr__(self, attr):
    return getattr(self.selenium, attr)


  def assertLocationEqual(self, location):
    self.assertEqual(self.selenium.get_location(), self.selenium.get_absolute_location(location))


  def assert_json(self, js_expr, expected_value):
    self.assertEqual(self.execute_javascript(js_expr, parse_json = True),
                     expected_value)

  def assert_js(self, js_expr, expected_value):
    self.assertEqual(self.execute_javascript(js_expr, parse_json = False),
                     expected_value)


  def tearDown(self):
    # Tim is awesome for helping with this bit.
    try:
      print "shutting down cherrypy"
      #self.server.httpd.requests.stop(0) # shutdown timeout?  pfft.
      print "shut down cherrypy"
    except socket.error:
      logging.info("Socket error stopping CherryPy requests")
    self.teardown_database(transactions = True)
    #self.stopped = True


  def _test_setup(self):
    """
    TestCase's _test_setup starts transactions and stuff, which we don't
    need, since we need to flush the database properly anyway (since
    if we're using this class, we'll be calling views, which have their
    own transaction management).
    """
    self._setup_urlconf()
    self.setup_database(transactions = True)

    self.server = CherryPyLiveServer(port = getattr(settings, "CHERRYPY_PORT", 8000))
    os.environ["PATH"] = "/usr/bin/firefox"
    self.selenium = ConvenientSelenium()


  def _test_teardown(self):
    """
    Taken from django.test.testcases.TestCase._fixture_teardown.
    We also stop the server.
    """
    self._teardown_urlconf()
    self.teardown_database(transactions = True)
    self.selenium.quit() 


  def post_last_teardown(self):
    self.server.stop()  

    for k, _ in self.get_selenium_settings().iteritems():
      setattr(settings, k, self.backup_settings[k])

    restore_database()


  def get_selenium_settings(self):
    return getattr(settings, "TEST_SETTINGS", {}).get("SELENIUM_SETTINGS", {})


class CherryPyLiveServer(object):
  """
  Starts a django server in the current process.

  This is really cool, because:
    - It makes selenium or urllib2 tests self-contained;
    - The test code and the server code run in the same process, and use the
      same database.  This means we can inject stuff into the database from the
      test code and the web server will know about it, and vice versa.

  SeleniumTestCase uses this but consumers of SeleniumTestCase shouldn't need
  to worry about it.

  Adapted from "django sane testing" 
    http://devel.almad.net/trac/django-sane-testing/wiki
  """

  def __init__(self, address = '0.0.0.0', port = 8000):
    _application = AdminMediaHandler(WSGIHandler())

    def application(environ, start_response):
      environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
      return _application(environ, start_response)

    self.httpd = CherryPyWSGIServer((address, port), 
                                    application, 
                                    server_name = 'localhost')

    self.httpd_thread = Thread(target=self.httpd.start)
    self.httpd_thread.start()

    self.server_started = True
    sleep(.5) # PURPLE

  def stop(self):
    if self.server_started:
      self.httpd.stop()
      self.server_started = False






