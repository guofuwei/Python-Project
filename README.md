# Python-Project

作为 Python 小组大作业的仓库

## 前端使用指南

#### 1.安装`flask`框架

```shell
pip install flask
```

#### 2.直接运行`python flask_client.py`即可

## 后端使用指南

### 1.安装运行环境

下面均以ubuntu环境举例

#### 安装 mysql

```shell
sudo apt-get update  #更新源
sudo apt-get install mysql-server #安装
```

#### 安装 redis

```shell
sudo apt update
sudo apt install redis-server
```

#### 安装 python 必要运行包

```shell
# 安装虚拟环境
pip install virtualenv`
# 创建虚拟文件夹并进入
virtualenv backend/venv`
# 激活虚拟环境并安装必需包
./backend/venv/bin/activate
pip install -r requirements.txt
```

### 2.迁移数据表格

```shell
# 记得修改backend/myblog/settings.py 下的mysql数据库设置
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 3.启动项目

```shell
python manage.py runserver
```

## Docker环境运行

### 1.安装docker和docker-compose

#### 安装docker

##### 卸载旧版本

```shell 
sudo apt-get remove docker docker-engine docker.io
```

##### 添加密钥及Docker软件源

```shell
sudo apt-get update && sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

##### 添加国内镜像源

```shell
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

```shell
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

##### 添加官方源

```shell
# 官方源
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

```shell
# 官方源
$ echo \
   "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

##### 安装Docker

```shell
sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io
```

##### 启动Docker

```shell
sudo systemctl enable docker && sudo systemctl start docker
```

##### 建立Docker用户组

```shell
sudo groupadd docker && sudo usermod -aG docker $USER
```

##### 配置镜像加速器

```shell
sudo mkdir -p /etc/docker
```

```shell
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://kzev4hva.mirror.aliyuncs.com"]
}
EOF
```

```shell
sudo systemctl daemon-reload
```

```shell
sudo systemctl restart docker
```

#### 安装docker-compose

打开以下网站：[docker/compose: Define and run multi-container applications with Docker (github.com)](https://github.com/docker/compose)

选择合适的版本并下载

重命名为`docker-compose`并 将其移到`/usr/local/bin`中

### 2.运行项目

修改前端static/config/config.js文件中的后端地址和后端myblog/settings.py中的mysql和redis地址

在项目根目录下运行`docker-compose up -d`即可
