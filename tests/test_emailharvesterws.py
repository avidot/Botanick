#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_botanick
----------------------------------

Tests for `botanick` module.
"""


from botanick import Botanick

def test_botanick():
	emails_found = Botanick.search("squad.pro")
	assert emails_found != ""
