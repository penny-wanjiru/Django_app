from django.conf import settings
from django.db.models.loading import get_model
from django.contrib.auth import authenticate, login


"""
TestBackend and TestUserMiddleware are convenient ways to
make the CherryPy server think a user has logged in.
"""
def get_user_model_class():
  return get_model(*settings.CUSTOM_USER_MODEL.split("."))

def get_forced_username():
  return settings.TEST_FORCE_USERNAME

def get_forced_email():
  return settings.TEST_FORCE_EMAIL

def get_forced_password():
  return settings.TEST_FORCE_PASSWORD


class TestAuthBackend(object): 
  supports_object_permissions = False
  supports_anonymous_user = True
  supports_inactive_user = False

  def authenticate(self, username=None, password=None):
    if not get_forced_username():
      return None

    klass = get_user_model_class()
    return klass.objects.get(username = get_forced_username())

  def get_user(self, user_id):
    return self.authenticate()


class TestUserMiddleware(object): 
  def process_request(self, request): 
    if "media" in request.path_info: # HACK
      return

    class Facebook:
      def __init__(self):
        self.uid = None
      def is_valid(self, request):
        return True
    request.facebook = Facebook()

    if not get_forced_username():
      # We can have a None get_forced_username, which means that the 
      # TestUserMiddleware should not operate.
      return

    user = authenticate(username = get_forced_username(),
                        password = get_forced_password())
    login(request, user)
    request.user = user



