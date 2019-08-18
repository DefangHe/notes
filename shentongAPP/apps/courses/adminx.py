import xadmin
from .models import *


class LessonInline(object):
    model = LessonInfo
    extra = 0


class CourseInfoXadmin(object):
    list_display = ['name', 'study_time', 'study_num', 'level', 'is_banner', 'love_num', 'click_num', 'category', 'image',
                    'orginfo', 'teacherinfo', 'add_time']
    list_filter = ['image', 'name', 'study_time', 'study_num', 'level', 'is_banner', 'love_num', 'click_num', 'category',
                   'orginfo', 'teacherinfo', 'add_time']
    search_fields = ['image', 'name', 'study_time', 'study_num', 'level', 'is_banner', 'love_num', 'click_num', 'category',
                     'orginfo', 'teacherinfo']
    model_icon = 'fa fa-hand-paper-o'
    readonly_fields = ['study_num', 'love_num']
    inlines = [LessonInline]


class LessonInfoXadmin(object):
    list_display = ['name', 'courseinfo', 'add_time']
    list_filter = ['name', 'courseinfo', 'add_time']
    search_fields = ['name', 'courseinfo']


class VideoInfoXadmin(object):
    list_display = ['name', 'study_time', 'url', 'add_time', 'lessoninfo']
    list_filter = ['name', 'study_time', 'url', 'add_time', 'lessoninfo']
    search_fields = ['name', 'study_time', 'url',  'lessoninfo']


class SourceInfoXadmin(object):
    list_display = ['name', 'down_load', 'courseinfo', 'add_time']
    list_filter = ['name', 'down_load', 'courseinfo', 'add_time']
    search_fields = ['name', 'down_load', 'courseinfo']


xadmin.site.register(CourseInfo, CourseInfoXadmin)
xadmin.site.register(LessonInfo, LessonInfoXadmin)
xadmin.site.register(VideoInfo, VideoInfoXadmin)
xadmin.site.register(SourceInfo, SourceInfoXadmin)
