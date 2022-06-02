#!/bin/bash
# 从第一行到最后一行分别表示：
# 1. 守护进程执行 celery，没有这个需求的小伙伴可以将第一行命令其删除
# 2. 收集静态文件到根目录，
# 3. 生成数据库可执行文件，
# 4. 根据数据库可执行文件来修改数据库
# 5. 用 gunicorn 启动 django 服务
# 6. 用 uwsgi 启动 django 服务
#celery -A celery_tasks.main worker -l info --logfile=./log/worker.log&&
#python3 manage.py collectstatic --noinput&&
# python manage.py makemigrations&&
python3 manage.py migrate&&
# gunicorn my_blog.wsgi:application -c gunicorn.conf
uwsgi --ini wsgi.ini
