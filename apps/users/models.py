from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self,mobile,username,password,**kwargs):
        if not mobile:
            raise ValueError('请传入手机号码！')
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')

        user = self.model(mobile=mobile,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,mobile,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(mobile,username,password,**kwargs)

    def create_superuser(self,mobile,username,password,**kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(mobile,username,password,**kwargs)

class Users(AbstractUser):
    """
    重写django自带的user表
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    name = models.CharField(max_length=10, verbose_name='姓名',null=True)


    class Meta:  # 配置数据库表名,及设置模型在admin站点显示的中文名
        db_table = 'fusion_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}".format(self.name)

