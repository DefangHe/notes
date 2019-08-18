from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from .models import UserProfile, EmailVerifyCode
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from Utils.email_send import send_register_email
from Utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
import json
from operations.models import UserCourse, UserLove, CourseInfo, UserMessage
from orgs.models import OrgInfo, TeacherInfo
from users.models import BannerInfo
from pure_pagination import Paginator, PageNotAnInteger


class ForgetPwdView(View):
    # 忘记密码
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {'forget_pwd_form': forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid:  # 是is_valid：而不是is_valid（）： 后面不能有括号！！！这个问题又是搞了一晚上
            email = request.POST.get("email", "")
            send_register_email(email, 'forget')
            return render(request, "send_success.html", {'forget_pwd_form': forget_pwd_form})
        else:
            return render(request, "forgetpwd.html", {'forget_pwd_form': forget_pwd_form})


class ResetView(View):
    # 密码重置
    def get(self, request, reset_code):
        all_records = EmailVerifyCode.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                print("过程hhh1")
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    # ResetView(View)要传active_code的参数，所以不能共用ResetView(View)
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')  # 密码修改成功，返回登录页面
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})


class ActiveUserView(View):
    # 账号激活
    def get(self, request, active_code):
        all_records = EmailVerifyCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):  # 账号注册
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid:
            user_name = request.POST.get("username", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"msg": "用户已存在", 'register_form': register_form})
            user_password = request.POST.get("password", "")
            user_profile = UserProfile()  # 一定要加（）！！！！！！这个问题我搞了一天才发现！！！
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(user_password)
            user_profile.save()

            # 发送注册成功消息
            user_message =  UserMessage()
            user_message.user = user_profile.id
            user_message.message_content = '欢迎注册加入神童研究院'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse("index"))  # 重定向，通过reverse把名称反转成url


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid:
            user_name = request.POST.get("username", "")
            user_password = request.POST.get("password", "")
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))  # 重定向，通过reverse把名称反转成url
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid:
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户头像修改
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    在个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"两次输入的密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')  # 密码修改成功
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    修改个人邮箱发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')  # 邮箱修改成功


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱提交表单
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyCode.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)  # 取用户的课程
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class MyLoveOrgView(LoginRequiredMixin, View):
    """
    我的收藏--机构
    """
    def get(self, request):
        org_list = []
        love_orgs = UserLove.objects.filter(user=request.user, love_type=1)  # 取用户的课程
        for love_org in love_orgs:
            org_id = love_org.love_id
            org = OrgInfo.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyLoveTeacherView(LoginRequiredMixin, View):
    """
    我的收藏--讲师
    """
    def get(self, request):
        teacher_list = []
        love_teachers = UserLove.objects.filter(user=request.user, love_type=3)  # 取收藏的讲师
        for love_teacher in love_teachers:
            teacher_id = love_teacher.love_id
            teacher = TeacherInfo.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyLoveCourseView(LoginRequiredMixin, View):
    """
    我的收藏--课程
    """
    def get(self, request):
        course_list = []
        love_courses = UserLove.objects.filter(user=request.user, love_type=2)  # 取收藏的课程
        for love_course in love_courses:
            course_id = love_course.love_id
            course = CourseInfo.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息
        all_unread_message = UserMessage.objects.filter(user=request.user.id, message_statue=False)
        for unread_message in all_unread_message:
            unread_message.message_statue = True
            unread_message.save()

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        P = Paginator(all_message, 6, request=request)
        messages = P.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })


class IndexView(View):
    """
    动态首页
    """
    def get(self, request):
        # 取出轮播图
        all_banners = BannerInfo.objects.all().order_by('index')
        courses = CourseInfo.objects.filter(is_banner=False)[:5]
        banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
        course_orgs = OrgInfo.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


def page_not_found(request, exception):
    """
    全局404处理函数
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    """
    全局404处理函数
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
