import xadmin
from .models import BannerInfo, EmailVerifyCode
from xadmin import views


class BaseXadminSetting(object):  # 配置主题
    enable_themes = True
    use_bootswatch = True


class GlobalXadminSetting(object):
    site_title = '神童公司后台管理系统'
    site_footer = '神童教育'
    menu_style = 'accordion'


class BannerInfoXadmin(object):
    list_display = ['title', 'index', 'image', 'url', 'add_time']
    search_fields = ['title', 'index', 'image', 'url']
    list_filter = ['title', 'index', 'image', 'url']


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']
    list_filter = ['code', 'email', 'send_type', 'add_time']
    search_fields = ['code', 'email', 'send_type']


xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)  # 注册主题类
xadmin.site.register(views.CommAdminView, GlobalXadminSetting)  # 注册样式类
