import hashlib

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect

from mainapp import models
import datetime


def register_form(request):
    '''
    渲染注册页面
    :param request:
    :return:
    '''
    return render(request, 'register.html')


def make_string(new_user):
    """
    用来给每一个用户生成一个唯一不可重的注册码
    :param new_user:当前用户
    :return:生成完成的验证码
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    h = hashlib.md5()
    code = new_user.name + now
    h.update(code.encode())
    code2 =h.hexdigest()
    models.ConfirmString.objects.create(code=code2, user=new_user)

    return code2


def send_email(email, code):
    """
    用来真正发送邮件发方法
    :param email:用户的邮箱号
    :param code:唯一的注册码
    :return:
    """
    subject, from_email, to = '欢迎注册当当网！', 'jsgao319@sina.com', email
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册！，<a href="http://{}/user/confirm/?email={}&code={}"target = blank >点击验证邮箱</a>，欢迎你来验证你的邮箱，验证结束你就可以登录了！ </p> '.format('127.0.0.1:8000', email, code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def email_main(user):
    """
    views.registlogic函数的组件，负责验证邮箱的业务处理
    :param user: 新建的对象
    :return:  处理user的email，发送验证邮件，成功则返回True,否则返回False
    """
    try:
        code = make_string(user)
        send_email(user.email, code)
    except:
        return False
    return True


def confirm(request):
    """
    用来处理用户点击邮箱中的连接来验证邮箱是否可用的视图
    :param request:邮箱确认请求
    :return:确认成功后直接变成已登陆状态，并跳转登陆界面
    """
    email = request.GET.get('email')
    code = request.GET.get('code')
    try:
        user = models.User.objects.get(email=email)
    except: # 用户不存在
        return HttpResponse('链接已失效')
    # 判断请求的注册码是否与数据库中该用户保存的一致
    old_code = user.confirmstring
    if code != old_code.code:
        return HttpResponse('链接已失效')
    # 将该用户的状态改为可用
    user.has_confirm = True
    user.save()
    # 删除注册码
    old_code.delete()

    # 直接登录，保存登录状态&用户名&用户id
    request.session['login_state'] = 'ok'
    request.session['login_user'] = email
    request.session['login_userid'] = user.id
    return render(request, 'userapp/register ok.html', {'username': email,
                                                        'login_state': request.session.get('login_state'),
                                                        'login_user': request.session.get('login_user'), })