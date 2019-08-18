# Generated by Django 2.2.1 on 2019-08-07 23:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='手机')),
                ('course', models.CharField(max_length=20, verbose_name='课程')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '咨询信息',
                'verbose_name_plural': '咨询信息',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_man', models.IntegerField(default=0, verbose_name='消息用户')),
                ('message_content', models.CharField(max_length=200, verbose_name='消息内容')),
                ('message_statue', models.BooleanField(default=False, verbose_name='消息状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='消息时间')),
            ],
            options={
                'verbose_name': '用户消息信息',
                'verbose_name_plural': '用户消息信息',
            },
        ),
        migrations.CreateModel(
            name='UserLove',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('love_id', models.IntegerField(verbose_name='收藏id')),
                ('love_type', models.IntegerField(choices=[(1, 'org'), (2, 'course'), (3, 'teacher')], verbose_name='收藏类别')),
                ('love_status', models.BooleanField(default=False, verbose_name='收藏状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间')),
                ('love_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='收藏用户')),
            ],
            options={
                'verbose_name': '收藏信息',
                'verbose_name_plural': '收藏信息',
            },
        ),
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.CharField(max_length=50, verbose_name='评论内容')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='评论时间')),
                ('comment_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseInfo', verbose_name='评论课程')),
                ('comment_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论用户')),
            ],
            options={
                'verbose_name': '用户评论课程信息',
                'verbose_name_plural': '用户评论课程信息',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='学习时间')),
                ('study_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseInfo', verbose_name='学习课程')),
                ('study_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='学习用户')),
            ],
            options={
                'verbose_name': '用户学习课程信息',
                'verbose_name_plural': '用户学习课程信息',
                'unique_together': {('study_man', 'study_course')},
            },
        ),
    ]
