# -*- coding: utf-8 -*-
"""Enums representing flags in the development cycle.

This is part of the python helpers library.

"""

from enum import Enum


class DevStatus(Enum):
    """Enum representing stages of development"""

    DEVELOPMENT = 0
    TESTING = 1
    PRODUCTION = 2
