# Python-Project

作为 Python 小组大作业的仓库

## 前端使用指南

### 测试环境

直接运行`python flask_client.py`即可

### 生产环境

可配合 nginx，用 nginx 反向代理 static 和 template 文件夹下的静态资源

## 后端使用指南

### 本机环境运行

#### 安装 mysql 和 redis 数据库，安装 python 必要运行包

##### 安装 mysql

##### 安装 redis

##### 安装 python 必要运行包

安装虚拟环境
`pip install virtualenv`
创建虚拟文件夹并进入
`virtualenv backend/venv`
激活虚拟环境并安装必需包
`./backend/venv/bin/activate`
`pip install -r requirements.txt`

##### 迁移数据表格

`cd backend`
`python manage.py makemigrations`
`python manage.py migrate`

#### 启动项目

`python manage.py runserver`
