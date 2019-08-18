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
from django.urls import path
from .views import *


urlpatterns = [
    path('info/', UserInfoView.as_view(), name="user_info"),
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    path('my_course/', MyCourseView.as_view(), name="my_course"),
    path('my_love/org/', MyLoveOrgView.as_view(), name="my_love_org"),
    path('my_love/teacher/', MyLoveTeacherView.as_view(), name="my_love_teacher"),
    path('my_love/course/', MyLoveCourseView.as_view(), name="my_love_course"),
    path('my_message/', MyMessageView.as_view(), name="my_message"),
]
