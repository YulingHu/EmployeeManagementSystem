import datetime

from django.db import models


# 用户表
class User(models.Model):
    username = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=50, default='')
    # 一个职位可以有多个员工
    position = models.ForeignKey('Position', on_delete=models.CASCADE, default='')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, default='')
    status = models.BooleanField(choices=((False, 'Not approve'), (True, 'In break')), default=False, verbose_name='Status')

    class Meta:
        db_table = 'user'

# 部门表
class Department(models.Model):
    department_name = models.CharField(max_length=10)

    class Meta:
        db_table = 'department'


# 职位表
class Position(models.Model):
    position = models.CharField(max_length=10)
    # 一个部门可以有多个职位
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    class Meta:
        db_table = 'position'


# 用户留言表
class LeavingMessage(models.Model):
    content = models.CharField(max_length=200)
    # 添加外键 默认关联User表的用户id
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    addtime = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'leavingmessage'

# 留言评论表
class Comment(models.Model):
    content = models.CharField(max_length=128, verbose_name='内容')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
    leavingmessage = models.ForeignKey('LeavingMessage', on_delete=models.CASCADE, verbose_name='留言')
    time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        db_table = 'comment'

# 公司通知表
class CompanyNotice(models.Model):
    content = models.TextField()
    addtime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class ApplyLeave(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
    reason = models.CharField(max_length=256, verbose_name='请假原因')
    status = models.BooleanField(choices=((False, '审核中'), (True, '已批准')), null=True)
    applydate = models.DateTimeField(auto_now_add=True, verbose_name='申请日期')