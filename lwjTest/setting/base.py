"""
Django settings for lwjTest project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import time
import datetime
from loguru import logger
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z+)h!p90^w&7c2_-hs9axv47c72z@6a*kb0#yuk$1s!2qew*o4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 允许可以访问的域名
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',#接口文档
    'apps.apiTest',#api
    'apps.report', #报告
    'apps.task',  #任务
    'apps.users', #用户
    'apps.verification', #验证码
    'apps.case',#用例
    'apps.system',#系统相关
    'apps.chanDao',#阐道
    'corsheaders',  # 跨域


]

MIDDLEWARE = [
    # 'utils.details.LoggerMiddleware',
    # 'utils.details.SentryMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'utils.details.CollectionMiddleware'
]

ROOT_URLCONF = 'lwjTest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lwjTest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {#mysql配置
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apitest',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
#redis配置
CACHES = {
    "default": {#缓存数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {#储存验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#继承了AbstractBaseUser，需要引用自定义的模型
AUTH_USER_MODEL = 'users.Users'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

#静态文件
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)



#url后面不用输入"/"
APPEND_SLASH=False

#logger日志配置
report_log_path = os.path.join(BASE_DIR, "../log")
today = time.strftime("%Y-%m-%d", time.localtime())
logging_file = os.path.join(report_log_path, "{}.log".format(today))
logger.add(
    logging_file,
    #格式
    format="{time:YYYY-MM-DD HH:mm:ss}|{level}|{message}",
    #文件最大大小
    rotation="500 MB",
    encoding="utf-8",
)

REST_FRAMEWORK= {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # JWT认证类  放在第一位是默认项
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

#jwt
JWT_AUTH = {
    # JWT有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 修改JWT登录视图的构造响应数据的函数
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.users.utils.jwt_response_payload_handler',
    # 我们传参数的时候开头自定义内容,注意点这里必须与下面的token中以宫格隔开
    'JWT_AUTH_HEADER_PREFIX': 'jwt',

}

# 修改Django用户认证后端类，为了实现多账号登录
AUTHENTICATION_BACKENDS = ['apps.users.utils.UsernameMobileAuthBackend']

#密码加密密钥
AES_KEY="fusiontests"

#公司邮箱配置
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.liweijia.com'
# EMAIL_PORT = 25
# #发送邮件的邮箱
# EMAIL_HOST_USER = 'wuhongbin@liweijia.com'
# #在邮箱中设置的客户端授权密码
# EMAIL_HOST_PASSWORD = 'fsqNsgyUhytkt9Jz'
# #收件人看到的发件人
# EMAIL_FROM = 'wuhongbin@liweijia.com'


#163邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'xiao_whb@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'AHVUDYGPCROYWUZJ'
#收件人看到的发件人
EMAIL_FROM = 'xiao_whb@163.com'


#服务器地址(用于测试报告)
HOST = "http://localhost:63342"

# 跨域问题
CORS_ORIGIN_ALLOW_ALL = True
 # 允许携带cookie
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:9528',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = [
    '*',
    'dnt',
    'source',
    'origin',
    'Pragma',
    'accept',
    'user-agent',
    'x-csrftoken',
    'X_FILENAME',
    'content-type',
    'authorization',
    'authentication',
    'XMLHttpRequest',
    'accept-encoding',
    "x-requested-with",
]
