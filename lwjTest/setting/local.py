# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/3/26 10:31 上午
from .base import *
DEBUG = True

DATABASES = {
    'default': {#mysql配置
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fusion_test1',
        'USER': 'root',
        'PASSWORD': 'xiaoxixi123',
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