# -*- coding: utf-8 -*-

import json
import requests
from gevent.pool import Pool
from flask import Flask, Response
from sqlalchemy import create_engine
from sqlalchemy import MetaData

from myapp.db import sqlalchemy_metadata
from sure.scenario import BehaviorDefinition, apply_behavior


# Changes in version 1.5.0 [draft]
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# * Introducing the concept of BehaviorDefinition: a clean and
#   decoupled way to reutilize setup/teardown behaviors. So instead of
#   the classic massive setup/teardown methods and/or chaotic
#   ``unittest.TestCase`` subclass inheritance every test can be
#   decorated with @apply_behavior(CustomBehaviorDefinitionTypeObject)
#
# * Avoid using the word "test" in your "Behavior Definitions" so that
#   nose will not mistake your BehaviorDefinition with an actual test
#   case class and thus execute .setup() and .teardown() in an
#   undesired manner.



def get_json_request(self):
    """parses the request body as JSON without running any sort of validation"""
    return json.loads(request.data)

def json_response(response_body, status=200, headers=None):
    """utility that automatically serializes the provided payload in JSON
    and generates :py:`flask.Response` with the ``application/json``
    content-type.

    :param response_body: a python dictionary or any JSON-serializable python object.

    """
    headers = headers or {}
    serialized = json.dumps(response_body, indent=2)
    headers[b'Content-Type'] = 'application/json'
    return Response(serialized, status=code, headers=headers)


class GreenConcurrencyBehaviorDefinition(BehaviorDefinition):
    # NOTE:
    # ----
    #
    # * Sure uses ``context_namespace`` internally to namespace the
    # self-assigned attributes into the context in order to prevent
    # attribute name collision.

    context_namespace = 'green'

    def setup(self, pool_size=1):
        self.pool = Pool(pool_size)


class UseFakeHTTPAPIServer(GreenConcurrencyBehaviorDefinition):
    context_namespace = 'fake_api'

    def setup(self, http_port):
        # NOTES:
        # ~~~~~~
        #
        # * GreenConcurrencyBehaviorDefinition.setup() is automatically called by
        # * sure in the correct order
        #
        # * Sure automatically takes care of performing top-down calls
        #   to every parent of your behavior.
        #
        # * In simple words, this UseFakeHTTPAPIServer behavior will automatically call GreenConcurrencyBehaviorDefinition

        # 1. Create a simple Flask server
        self.server = Flask('fake.http.api.server')
        # 2. Setup fake routes
        self.server.add_url_rule('/auth', view_func=self.fake_auth_endpoint)
        self.server.add_url_rule('/item/<uid>', view_func=self.fake_get_item_endpoint)
        # 3. Run the server
        self.pool.spawn(self..server.run, port=http_port)

    def teardown(self):
        self.server.stop()

    def fake_auth_endpoint(self):
        data = get_json_request()
        data['token'] = '$2b$12$heKIpWg0wJQ6BeKxPSJCP.7Vf9hn8s6yFs8yGWnWdPZ48toXbjK9W',
        return json_response(data)

    def fake_get_item_endpoint(self, uid):
        return json_response({
            'uid': uid,
            'title': 'fake item',
        })


class CleanSlateDatabase(BehaviorDefinition):
    # Sure uses ``context_namespace`` internally to namespace the
    # self-assigned attributes into the context in order to prevent
    # attribute name collision
    context_namespace = 'db'

    def setup(self, sqlalchemy_database_uri='mysql://root@localhost/test-database'):
        self.engine = create_engine(sqlalchemy_database_uri)
        self.metadata = sqlalchemy_metadata
        # Dropping the whole schema just in case a previous test
        # execution fails and leaves the database dirty before having
        # the chance to run .teardown()
        self.metadata.drop_all(engine)
        self.metadata.create_all(engine)


@apply_behavior(UseFakeHTTPAPIServer, http_port=5001)
def test_with_real_network_io(context):
    response = requests.post('http://localhosst:5001/auth', data=json.dumps({'username': 'foobar'}))
    response.headers.should.have.key('Content-Type').being.equal('application/json')
    response.json().should.equal({
        'token': '$2b$12$heKIpWg0wJQ6BeKxPSJCP.7Vf9hn8s6yFs8yGWnWdPZ48toXbjK9W',
        'username': 'foobar',
    })
