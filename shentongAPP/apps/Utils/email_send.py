from users.models import EmailVerifyCode
from random import Random
from django.core.mail import send_mail
from shentongAPP.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyCode()  # 一定要加（）！！！！！！这个问题我搞了一天才发现！！！
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        email_title = "神童研究院注册程序"
        email_body = "请点击下方链接进入实验室注册空间：http://127.0.0.1:8000/active/{0}".format(code)
        send_stats = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_stats:
            pass
    elif send_type == 'forget':
        email_title = "神童研究院密码重置系统"
        email_body = "请点击下方链接进入实验室重置密码空间：http://127.0.0.1:8000/reset/{0}".format(code)
        send_stats = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_stats:
            pass

    elif send_type == 'update_email':
        email_title = "神童研究院邮箱修改系统"
        email_body = "你的邮箱验证码为：{0}".format(code)
        send_stats = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_stats:
            pass


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
