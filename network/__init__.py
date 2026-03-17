# -*- coding: utf-8 -*-
# network/__init__.py
# 网络通信模块初始化
from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)
# TODO:需要从数据库替换该名字
username = "admin"
# 首页
@app.route("/")
def index():
    return render_template("index.html", username=username)

# 图表页
@app.route("/chart_page")
def chart_page():
    return render_template("chart.html", username=username)

#用户页
@app.route("/setting")
def setting():
    return render_template("setting.html", username= username)


# 导入 API
from . import server