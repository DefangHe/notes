from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=25,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少为三位',
                                   'max_length': '密码最多为25位'
                               })


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=25,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少为三位',
                                   'max_length': '密码最多为25位'
                               })
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=3, max_length=25,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少为三位',
                                   'max_length': '密码最多为25位',
                               })
    password2 = forms.CharField(required=True, min_length=3, max_length=25,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少为三位',
                                   'max_length': '密码最多为25位',
                               })


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'phone']
