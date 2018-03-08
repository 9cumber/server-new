# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
