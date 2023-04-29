# flake8: noqa
# -*- coding: utf-8 -*-

# ===========================================
# Behavior definition examples in pseudo code
# ===========================================


####################################################################################

# UNIT TESTS
# ---------

# Goals:
# ~~~~~
#
# * Provide an API that leverages mocking ``sure.scenario.MockfulBehaviorDefinition``
# * Provide a didactic and fun way to keep the mocks organized
# * Make monkey-patching of modules more fun:
#   * Always forward the mocked objects as keyword-arguments as
#     opposed to the default behavior of ``@patch()`` decorator stack
#     which uses positional arguments, polute test declarations and
#     demands menial, extrenuous work in case of test refactoring.
#   * ``self.mock.module(members={})`` is a shorthand for creating a dummy module object that contains the given members as properties

# Notes:
# ~~~~~
#
# * the following methods require exactly one positional argument: ``mock_name``, otherwise: ``raise AssertionError("self.mock.simple() and self.mock.magic() require one positional argument: its name.")``
#   * ``self.mock.simple()``
#   * ``self.mock.magic()``
# * self.mock.install() forwards keyword-arguments to ``mock.patch``, for example:
#   * ``self.mock.install('myapp.api.http.db.engine.connect', return_value='DUMMY_CONNECTION')
#   * ``self.mock.install('myapp.api.http.db.engine.connect', return_value='DUMMY_CONNECTION')
# * self.mock.install() always generates MagicMocks
# * self.mock.install() accepts the parameter ``argname='some_identifier`` to be passed the keyword-argument that contains the ``Mock`` instance returned by ``.install()``
# * When ``argname=None`` the mock instance will be passed with a keyword-arg whose value is derived from the last __name__ found in the patch target, that is: ``self.mock.install('myapp.core.BaseServer')`` will change the test signature to: ``def test_something(context, BaseServer)``.
# * self.mock.install() will automatically name the mock when the ``name=""`` keyword-arg is not provided
# * self.mock.uninstall() accepts one positional argument: identified and then automatically match it against:
# * self.scenario.forward_argument() allows for arbitrary parameters in the test function, that is: ``self.scenario.forward_argument(connection=self.connection)`` will change the test signature to: ``def test_something(context, connection)``.
# * Developers do *NOT* need to manually uninstall mocks, but that is
#   still permitted to encompass the cases where it has to be
#   accomplished in mid-test, for example:
#
#   @apply_behavior(FakeSettings)
#   @apply_behavior(PreventRedisIO)
#   def test_something(context):
#       # perform some action that requires a stubbed setting
#       context.redis.mock.uninstall(name='
#       # peform
#

# <unit-test-example-pseudo-code>
from mock import Mock
from myapp import settings
from myapp.api.http import APIServer
from sure.scenario import MockfulBehaviorDefinition, apply_behavior, require_behavior


class FakeSettings(MockfulBehaviorDefinition):
    """automatically patches myapp.settings and overriding its keys with
    the provided kwargs."""

    context_namespace = 'settings'

    def setup(self, **kwargs):
        # 1. make 2 copies:
        #    * one original copy for backup
        #    * one containing the overrides
        self.original_state = settings.to_dict()
        cloned_state = settings.to_dict()

        # 2. Apply the overrides in the cloned state
        cloned_state.update(kwargs)

        # 3. Create a module mock containing the members
        fake_settings = self.mock.module(members=fake_state)

        # 4. Install the mocked settings
        self.mock.install('myapp.api.http.settings', fake_settings)


class PreventRedisIO(MockfulBehaviorDefinition):
    context_namespace = 'redis'

    def setup(self):
        self.connection = self.mock.simple('redis-connection-instance')
        self.mock.install('myapp.api.http.RedisConnection', argname='connection', return_value=self.connection)

class PreventSQLIO(MockfulBehaviorDefinition):
    context_namespace = 'sql'

    def setup(self):
        self.engine = self.mock.simple('sqlalchemy.engine')
        self.connection = self.engine.return_value
        self.mock.install('myapp.api.http.sqlengine', return_value=self.engine)
        self.scenario.forward_argument(connection=self.connection)


class IOSafeAPIServer(BehaviorGroup):
    layers = [
        FakeSettings(SESSION_SECRET='dummy'),
        PreventRedisIO(),
        PreventSQLIO()
    ]


@apply_behavior(IOSafeAPIServer)
def test_api_get_user(context, connection, ):
    ('APIServer.handle_get_user() should try to retrieve from the redis cache first')

    # Given a server
    api = APIServer()

    # When I call .handle_get_user()
    response = api.handle_get_user(user_uuid='b1i6c00010ff1ceb00dab00b')

    # Then it should have returned a response
    response.should.be.a('flask.Response')
