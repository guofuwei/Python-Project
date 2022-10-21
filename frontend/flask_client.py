'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-14 09:14:48
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-20 13:17:08
FilePath: /Python-Project/frontend/flask_client.py
Description: flask框架代理博客网站前端页面

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''


from flask import Flask, send_file
import sys


app = Flask(__name__)


@app.route('/')
def default():
    """默认界面

    Returns:
        html: index
    """
    return send_file('templates/index.html')


@app.route('/index')
def index():
    """index 页面

    Returns:
        html: index
    """
    return send_file('templates/index.html')


@app.route('/login')
def login():
    """登陆 页面

    Returns:
        html: login
    """
    return send_file('templates/login.html')


@app.route('/login_callback')
def login_callback():
    """登陆回调 页面

    Returns:
        html: oauth_callback
    """
    return send_file('templates/oauth_callback.html')


@app.route('/register')
def register():
    """注册 页面

    Returns:
        html: register
    """
    return send_file('templates/register.html')


@app.route('/<username>/info')
def info(username):
    """个人信息 页面

    Returns:
        html: about
    """
    return send_file('templates/about.html')


@app.route('/<username>/change_info')
def change_info(username):
    """修改个人信息 页面

    Returns:
        html: change_info
    """
    return send_file('templates/change_info.html')


@app.route('/<username>/change_password')
def change_password(username):
    """修改密码 页面

    Returns:
        html: change_password
    """
    return send_file('templates/change_password.html')


@app.route('/<username>/topic/release')
def topic_release(username):
    """发表博客 页面

    Returns:
        html: release
    """
    return send_file('templates/release.html')


@app.route('/<username>/topics')
def topics(username):
    """个人博客列表 页面

    Returns:
        html: list
    """
    return send_file('templates/list.html')


@app.route('/<username>/topics/detail/<t_id>')
def topics_detail(username, t_id):
    """博客内容详情 页面

    Returns:
        html: detail
    """
    return send_file('templates/detail.html')


@app.route('/test_api')
def test_api():
    """测试 页面

    Returns:
        html: test_api
    """
    return send_file('templates/test_api.html')


@app.route('/test')
def test():
    """测试 页面

    Returns:
        html: test
    """
    # 测试
    return send_file('templates/test.html')


@app.route('/<username>/topic/release_update/<t_id>')
def release_update(username, t_id):
    """修改文章 页面

    Returns:
        html: release_update
    """
    return send_file('templates/release_update.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
