from flask import Flask, render_template, url_for, redirect
import os

from .database import *

# from .database import query

app = Flask(__name__)

app.config.from_object('config')

# from app.mod_pages.controllers import mod_pages as pages_module
#
# app.register_blueprint(pages_module)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.route('/')
def a():
    return redirect('/index')


@app.route('/index')
def index():
    months, data_bar = get_money_by_month()
    type, data_pie = get_money_by_type()
    return render_template('/index.html',
                           tongtien=get_tongtien(),
                           tongtheothang=get_tongtientheothang(),
                           donht=get_demdonht(),
                           donchuaht=get_donchuaht(),
                           months=months,
                           data_bar=data_bar,
                           type=type,
                           data_pie=data_pie)


@app.route('/tkds')
def tkds():
    return render_template('/tkds.html')


@app.route('/qldh')
def qldh():
    return render_template('/qldh.html', list_dh=get_dsdonhang())


@app.route('/qlkh')
def qlkh():
    return render_template('/qlkh.html', users=get_user())


@app.route('/qlsp')
def qlsp():
    return render_template('/qlsp.html', products=get_product())