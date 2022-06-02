from django.db import models
from ..apiTest.models import Project
class FormalBug(models.Model):
    """
    现网bug
    """
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属的项目')
    question = models.CharField(max_length=1000,verbose_name="问题")
    reason = models.CharField(max_length=1000,verbose_name="原因")
    discoverer = models.CharField(null=True,max_length=10,verbose_name="发现人")
    solve_time = models.CharField(max_length=100,null=True,blank=True,verbose_name="解决时间")

    class Meta:
        db_table = "fusion_formal_bug"
        verbose_name = "现网漏侧问题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question

class SyetemQuestion(models.Model):
    """
    系统问题
    """
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属的项目')
    question = models.CharField(max_length=1000,verbose_name="问题")
    handle = models.CharField(max_length=1000,verbose_name="如何处理")

    class Meta:
        db_table = "fusion_question"
        verbose_name = "系统问题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project
