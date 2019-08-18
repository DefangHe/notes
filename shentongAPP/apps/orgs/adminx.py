import xadmin
from .models import *


class CityInfoXadmin(object):
    list_display = ['name', 'add_time']
    list_filter = ['name', 'add_time']
    search_fields = ['name']
    model_icon = 'fa fa-bank'


class OrgInfoXadmin(object):
    list_display = ['image', 'name', 'course_num', 'cityinfo', 'study_num', 'love_num', 'click_num', 'category']
    list_filter = ['image', 'name', 'course_num', 'cityinfo','study_num', 'love_num', 'click_num', 'category']
    search_fields = ['image', 'name', 'course_num', 'cityinfo','study_num', 'love_num', 'click_num', 'category']
    model_icon = 'fa fa-user'


class TeacherInfoXadmin(object):
    list_display = ['image', 'name', 'work_year', 'work_position', 'work_style', 'click_num', 'age',
                    'gender', 'love_num']
    list_filter = ['image', 'name', 'work_year', 'work_position', 'work_style', 'click_num', 'age',
                    'gender', 'love_num']
    search_fields = ['image', 'name', 'work_year', 'work_position', 'work_style', 'click_num', 'age',
                    'gender', 'love_num']
    model_icon = 'fa fa-gift'


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
