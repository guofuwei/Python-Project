FROM python
WORKDIR /app
COPY . /app
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list;\
    apt-get clean;\
    apt-get install libmysqlclient-dev gcc python3-dev;\
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple;\
    python -m pip install --upgrade pip;\
    pip install -r requirement.txt
