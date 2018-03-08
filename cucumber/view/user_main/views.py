# encoding: utf-8
from . import main
from jinja2 import Environment, FileSystemLoader
from flask import session, request, redirect, url_for, render_template
from ..models import User

jinja = Environment(loader=FileSystemLoader('app/assets', encoding='utf8'))
"""
トップページ
"""


@main.route('/')
def index():
    # ログインしていたら
    if 'email' in session:
        # message = "Hi " + session['email']
        t = jinja.get_template('dashboard.html')
        body = t.render()
        return body
        # return message
    else:
        t = jinja.get_template('index.html')
        return render_template('index.html')


@main.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    admin = User.fetch(email, password)
    if admin is None:
        return 'ユーザが存在しません'

    session['email'] = email  # ログインしたことにする
    return redirect(url_for('main.index'))


@main.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)  # ログアウトしたことにする
    return redirect(url_for('main.index'))
