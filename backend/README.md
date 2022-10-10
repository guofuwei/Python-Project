#celery后台启动

# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES="worker1"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
#CELERYD_NODES=10
 
# Absolute or relative path to the 'celery' command:如果是虚拟环境中的celery则应写作 /opt/virtualenv/bin/celery
CELERY_BIN="/home/ubuntu/blogsite/venv_blog/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"
 
# App instance to use
# comment out this line if you don't use an app ,在diango中实例化celery app时的name
CELERY_APP="myblog"
# or fully qualified:
#CELERY_APP="proj.tasks:app"
 
# Where to chdir at start.对于django项目来说，用于创建celery app的文件celery.py的目录为 /opt/Myproject/Myproject/celery.py ,该目录用于查找celery app 
CELERYD_CHDIR="/home/ubuntu/blogsite/blogsitev1/myblog2/"
 
# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"
 
# Set logging level to DEBUG
#CELERYD_LOG_LEVEL="DEBUG"
 
# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
 
# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists (e.g., nobody).这里的用户名，用于运行celery的非root user 与 用户组
CELERYD_USER="celery"
CELERYD_GROUP="celery"
 
# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1



# /home/ubuntu/blogsite/blogsitev1/myblog2/celeryd.log
