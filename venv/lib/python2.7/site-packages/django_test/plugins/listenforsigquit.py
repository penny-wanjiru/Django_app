from django_test.plugins import Plugin

class ListenForSigQuitPlugin(Plugin):
  def init(self, test_driver):
    from playfi.util.debug import listen_for_sigquit
    listen_for_sigquit()


