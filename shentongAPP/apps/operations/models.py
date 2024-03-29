from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import CourseInfo
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=30, verbose_name="姓名")
    phone = models.CharField(max_length=11, verbose_name="手机")
    course = models.CharField(max_length=20, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '咨询信息'
        verbose_name_plural = verbose_name


class UserLove(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="收藏用户", on_delete=models.CASCADE)
    # 收藏用户名字必须为user，否则在写用户收藏view的时候会出错！
    love_id = models.IntegerField(verbose_name="收藏id")
    love_type = models.IntegerField(choices=((1, 'org'), (2, 'course'), (3, 'teacher')), verbose_name="收藏类别")
    love_status = models.BooleanField(default=False, verbose_name="收藏状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '收藏信息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="学习用户", on_delete=models.CASCADE)
    study_course = models.ForeignKey(CourseInfo, verbose_name="学习课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="学习时间")

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'study_course')
        verbose_name = '用户学习课程信息'
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="评论用户", on_delete=models.CASCADE)
    comment_course = models.ForeignKey(CourseInfo, verbose_name="评论课程", on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=50, verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    def __str__(self):
        return self.comment_content

    class Meta:
        verbose_name = '用户评论课程信息'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="消息用户")
    message_content = models.CharField(max_length=200, verbose_name="消息内容")
    message_statue = models.BooleanField(default=False, verbose_name="消息状态")  # False为未读
    add_time = models.DateTimeField(default=datetime.now, verbose_name="消息时间")

    def __str__(self):
        return self.message_content

    class Meta:
        verbose_name = '用户消息信息'
        verbose_name_plural = verbose_name
