import xadmin
from .models import *


class UserAskXadmin(object):
    list_display = ['name', 'phone', 'course', 'add_time']
    list_filter = ['name', 'phone', 'course', 'add_time']
    search_fields = ['name', 'phone', 'course']


class UserLoveXadmin(object):
    list_display = ['user', 'love_id', 'love_type', 'love_status', 'add_time']
    list_filter = ['user', 'love_id', 'love_type', 'love_status', 'add_time']
    search_fields = ['user', 'love_id', 'love_type', 'love_status']


class UserCourseXadmin(object):
    list_display = ['user', 'study_course', 'add_time']
    list_filter = ['user', 'study_course', 'add_time']
    search_fields = ['user', 'study_course']


class UserCommentXadmin(object):
    list_display = ['user', 'comment_course', 'comment_content', 'add_time']
    list_filter = ['user', 'comment_course', 'comment_content', 'add_time']
    search_fields = ['user', 'comment_course', 'comment_content']


class UserMessageXadmin(object):
    list_display = ['user', 'message_content', 'message_statue', 'add_time']
    list_filter = ['user', 'message_content', 'message_statue', 'add_time']
    search_fields = ['user', 'message_content', 'message_statue']
    model_icon = 'fa fa-envelope-open'


xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(UserLove, UserLoveXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserComment, UserCommentXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
