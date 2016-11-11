#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_botanick
----------------------------------

Tests for `botanick` module.
"""

import pytest


from botanick import Botanick

def test_botanick():
	emails_found = Botanick.search("squad.pro")
	assert emails_found != ""
	print(emails_found)
