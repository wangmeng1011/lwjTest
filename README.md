## 执行命令
>celery的运行：celery -A celery_tasks.main worker -l info
> 超级管理员：python3 manage.py createsuperuser
>本地启动服务：python3 manage.py runserver --settings=fusionTest.setting.local
>dev启动服务：python3 manage.py runserver --settings=fusionTest.setting.dev
>staging启动服务：python3 manage.py runserver --settings=fusionTest.setting.staging


## mixins试图工具集
>RetrieveModelMixin：retrieve 单取
>ListModelMixin：list 群取
>CreateModelMixin：create 单增
>UpdateModelMixin：update 单整体改
>UpdateModelMixin: partial_update 单局部改
>DestroyModelMixin：destroy 单删


##admin站点
>登录使用username，密码未加密

##平台登录
>登录使用mobile，密码加密方式aes+base64

#认证
>采取jwt认证，登录后返回token，在请求头传{"Authorization":"jwt {token}"}

#异步任务
>1发送验证码
>2发送邮箱


#选型
>语言：python
>后端框架：django rest framework
>单元测试框架：unittest
>前端框架：vue
>数据库：mysql,redis
>任务调度：celery、scheduler
>认证：jwt
>报告：BeautifulReport


 
#部署
1. 从官方拉取python基础镜像到服务器的镜像仓库
2. 生成django镜像
3. 生成容器



