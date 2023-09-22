#!/usr/bin/env python3
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

from typing import List
from pathlib import Path

from sure.importer import importer

module_root = Path(__file__).parent.absolute()

REPORTERS = {}
AGENTS = {}
ACTORS = {}


def add_agent(agent: type) -> type:
    AGENTS[agent.name] = agent
    return agent


def get_agent(name: str) -> type:
    return AGENTS.get(name)


def gather_agent_names() -> List[str]:
    return list(filter(bool, AGENTS.keys()))


def add_actor(actor: type) -> type:
    ACTORS[actor.name] = actor
    return actor


def get_actor(name: str) -> type:
    return ACTORS.get(name)


def gather_actor_names() -> List[str]:
    return list(filter(bool, ACTORS.keys()))


def add_reporter(reporter: type) -> type:
    if reporter.name == "__meta__":
        return reporter

    REPORTERS[reporter.name] = reporter
    return reporter


def get_reporter(name: str) -> type:
    return REPORTERS.get(name)


def gather_reporter_names() -> List[str]:
    return list(filter(bool, REPORTERS.keys()))


def internal_module_name(name):
    return __name__.replace(".meta", f".{name}.")


def register_class(cls, identifier):
    cls.kind = identifier
    cls.importer = importer
    if len(cls.__mro__) > 2:
        register = MODULE_REGISTERS[identifier]
        return register(cls)
    else:
        return cls


MODULE_REGISTERS = dict(
    (
        ("reporter", add_reporter),
        ("agent", add_agent),
        ("actor", add_actor),
    )
)


class MetaActor(type):
    def __init__(cls, name, bases, attrs):
        if cls.__module__ != __name__:
            cls = register_class(cls, "actor")

        super(MetaActor, cls).__init__(name, bases, attrs)


class MetaReporter(MetaActor):
    def __init__(cls, name, bases, attrs):
        cls = register_class(cls, "reporter")
        super(MetaReporter, cls).__init__(name, bases, attrs)


class MetaAgent(MetaActor):
    def __init__(cls, name, bases, attrs):
        if cls.__module__ != __name__:
            cls = register_class(cls, "agent")

        super(MetaAgent, cls).__init__(name, bases, attrs)
