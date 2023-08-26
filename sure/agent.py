#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2023>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

from sure.meta import get_agent, MetaAgent, gather_agent_names
from sure.actors import Actor
__path__ = os.path.abspath(os.path.dirname(__file__))


class Agent(Actor):
    """Base class for agents.

    The following optional methods should be implemented:

    * :py:meth:`~sure.agent.Agent.on_wake`
    * :py:meth:`~sure.agent.Agent.on_sleep`
    * :py:meth:`~sure.agent.Agent.on_consume`
    * :py:meth:`~sure.agent.Agent.on_produce`
    * :py:meth:`~sure.agent.Agent.on_communication_error`
    """
    __metaclass__ = MetaAgent
    name = None

    def __init__(self, runner, ):
        self.runner = runner

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def on_present(self):
        """Called as soon as `sure' starts running.

        .. code:: python

           from sure.agent import Agent

           output = open('/dev/random', 'ba')

           class HelloAgent(Agent):
               def on_start(self):
                   output.write(b"sure's test runner has started")

           HelloAgent(':py:class:`sure.runner.Runner`').on_start()
        """

    def on_finish(self):
        """Called as soon as `sure' finishes running.

        .. code:: python

           from sure.agent import Agent

           output = open('/dev/random', 'ba')

           class HelloAgent(Agent):
               def on_finish(self):
                   output.close()

           HelloAgent(':py:class:`sure.runner.Runner`').on_finish()
        """

    def on_feature(self):
        """Called as soon as `sure' finishes running.

        .. code:: python

           from sure.agent import Agent

           output = open('/dev/random', 'ba')

           class HelloAgent(Agent):
               def on_finish(self):
                   output.close()

           HelloAgent(':py:class:`sure.runner.Runner`').on_finish()
        """
