"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    re_path('home/(?P<org_id>\d+)', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)', OrgCourseView.as_view(), name='org_course'),
    re_path('desc/(?P<org_id>\d+)', OrgDescView.as_view(), name='org_desc'),
    re_path('teacher/(?P<org_id>\d+)', OrgTeacherView.as_view(), name='org_teacher'),  # 机构讲师
    # 机构收藏
    path('add_love/', AddLoveView.as_view(), name='add_love'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    re_path('teacher/detail/(?P<teacher_id>\d+)', TeacherDetailView.as_view(), name='teacher_detail'),  # 讲师详情
]
