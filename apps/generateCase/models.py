from django.db import models
# 请求方法枚举
HTTP_METHOD_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)

# 请求类型
REQUEST_TYPE = (
    ('json', 'json'),
    ('data', 'data')
)

class GenerateCaseName(models.Model):
    """
    导入名称
    """
    name = models.CharField(max_length=100, verbose_name="用例名称")
    is_delete = models.BooleanField(default=False,verbose_name="标记删除")
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    project = models.CharField(max_length=100,blank=True,verbose_name="系统")
    class Meta:
        db_table = "fusion_generate_case_name"
        verbose_name="导入用例名称"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.name)

class GenerateCase(models.Model):
    """
    导入测试用例
    """

    host = models.CharField(max_length=100, verbose_name="域名")
    path = models.CharField(max_length=1000, verbose_name="请求路径")
    method = models.CharField(max_length=100,choices=HTTP_METHOD_CHOICE,verbose_name="请求方法")
    request_type = models.CharField(max_length=100, choices=REQUEST_TYPE, verbose_name="请求类型")
    data = models.CharField(max_length=5000, verbose_name="请求参数")
    headers = models.CharField(max_length=5000, verbose_name="请求头")
    #argumentExtract格式
    # [{"name":"","origin":"","format":""},{"name":"","origin":"","format":""}]
    argumentExtract = models.CharField(max_length=2000, verbose_name="参数提取",blank=True)
    expect_code = models.IntegerField(verbose_name="预期状态码")
    #expect_content格式
    # [{"name":"","value":""},{"name":"","value":""}]
    expect_content = models.CharField(max_length=2000, verbose_name="断言内容",blank=True)
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    name = models.ForeignKey(GenerateCaseName, on_delete=models.CASCADE, verbose_name='用例名称',null=True,related_name='step')
    sleep_time=models.IntegerField(verbose_name="等待时间",default=0)
    remarks = models.CharField(max_length=1000,verbose_name="备注",blank=True)

    class Meta:
        db_table = "fusion_generate_case"
        verbose_name="导入接口用例"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.path)

class GenerateCaseRunRecord(models.Model):
    """
    用例运行记录
    """
    name = models.ForeignKey(GenerateCaseName,on_delete=models.CASCADE,verbose_name='用例名称')
    create_time = models.DateTimeField(auto_now=True,verbose_name='运行时间')
    class Meta:
        ordering = ['-create_time']
        db_table = "fusion_generate_run_record"
        verbose_name="用例运行记录"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.name)

class GenerateRunStepRecord(models.Model):
    """
    用例步骤记录
    """
    url = models.CharField(max_length=200,verbose_name='请求的url')
    http_method = models.CharField(max_length=10, verbose_name='请求方式', choices=HTTP_METHOD_CHOICE)
    data = models.TextField(blank=True,null=True,verbose_name='提交的数据')
    headers = models.TextField(blank=True,null=True,verbose_name='提交的header')
    runTime = models.CharField(max_length=200,verbose_name='运行的时间')
    return_code = models.CharField(max_length=10,verbose_name='返回的code')
    return_content = models.TextField(blank=True,null=True, verbose_name='返回的内容')
    return_cookies = models.TextField(blank=True,null=True, verbose_name='返回的cookies')
    return_headers = models.TextField(blank=True,null=True, verbose_name='返回的headers')
    case = models.ForeignKey(GenerateCaseRunRecord,on_delete=models.SET_NULL,blank=True, null=True,verbose_name='用例名称')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    api = models.ForeignKey(GenerateCase,on_delete=models.SET_NULL,blank=True, null=True,verbose_name='api')

    class Meta:
        ordering = ['create_time']
        db_table = "fusion_generate_step_record"
        verbose_name="api运行记录"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.url)
