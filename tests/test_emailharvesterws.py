#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_emailharvesterws
----------------------------------

Tests for `emailharvesterws` module.
"""

import pytest


from emailharvesterws import EmailHarvesterWS

def test_emailharvesterws():
	emails_found = EmailHarvesterWS.search("squad.pro")
	assert emails_found != ""
	print(emails_found)
