#!/usr/bin/env python
# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import click
from flask.cli import FlaskGroup

def create_app(_=None):
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass

@cli.command()
def list_routes():
    """
        List routes (like Rail's rake routes)
        this snippets refer to http://ominian.com/2017/01/17/flask-list-routes-rake-equivalent/ 
    """
    format_str = lambda *x: "{:30s} {:40s} {}".format(*x)  #pylint: disable=W0108
    from collections import defaultdict
    clean_map = defaultdict(list)

    for rule in cli.create_app().url_map.iter_rules():
        methods = ",".join(rule.methods)
        clean_map[rule.endpoint].append((methods, str(rule), ))

    print(format_str("View handler", "HTTP METHODS", "URL RULE"))
    print("-" * 80)
    for endpoint in sorted(clean_map.keys()):
        for rule, methods in sorted(clean_map[endpoint], key=lambda x: x[1]):
            print(format_str(endpoint, methods, rule))


if __name__ == '__main__':
    cli()
