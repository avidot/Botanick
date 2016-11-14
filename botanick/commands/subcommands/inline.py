# -*- coding: utf-8 -*-
from botanick.core.harvester import harvest
from botanick.core.converters import tostring


def inline(args):
    print(tostring(harvest(args['domain'])))
