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
from django.conf.urls import include
import xadmin
from users.views import *
from orgs.views import OrgView
from django.views.static import serve
# from shentongAPP.settings import MEDIA_ROOT, STATIC_ROOT
from shentongAPP.settings import MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('course/', include(('courses.urls', 'courses'), namespace='courses')),
    path('org/', include(('orgs.urls', 'orgs'), namespace='org')),
    path('operations/', include(('operations.urls', 'operations'), namespace='operations')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),  # 动态匹配，用re_path
    path('forget_pwd/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<reset_code>.*)/', ResetView.as_view(), name='reset_pwd'),  # 动态匹配，用re_path
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),  # 配置上传文件的访问处理函数
    # 必须是r'media/(?P<path>.*)$'才能显示，'media/(?P<path>.*)/'无法显示

  #  re_path(r'statics/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),  # 全局404配置 生产模式
]


# 全局404配置
handler404 = page_not_found
handler500 = page_error
