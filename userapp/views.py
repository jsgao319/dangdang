import hashlib

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from mainapp.models import *
import random,string

from userapp.email_part import *
from .captcha.image import ImageCaptcha


def regist(request):
    '负责渲染注册页面的函数'
    return render(request, 'userapp/register.html',{'login_state': request.session.get('login_state'),
                                                    'login_user': request.session.get('login_user'),})

def username_check(request):
    '处理用户名重复的ajax请求'
    username = request.GET.get('username')      #请求查询的目标
    res = User.objects.filter(name=username)    #查询数据库有没有该目标
    print('username:',username,res)
    if res:
        return HttpResponse('exist')    # 用户名已存在
    return HttpResponse('ok')

def captcha(request):
    '负责产生验证码的函数'
    image = ImageCaptcha()      #创建img对象
    code = random.sample(string.ascii_letters + string.digits, 4)   # 从string.ascii_letters + string.digits中产生4个随机字符
    random_code = ''.join(code) #拼接在一起
    print(random_code)
    request.session['captcha'] = random_code    #存在session中
    data = image.generate(random_code)  #将验证码渲染到图片中
    return HttpResponse(data)   #返回验证码图片

def cap_get(request):
    'ajax请求验证码'
    cap_old = request.session.get('captcha')    #从session中读取并返回
    return HttpResponse(cap_old)


def registlogic(request):
    '注册逻辑'
    # 获取表单中的参数
    username = request.POST.get('username')     # 就是邮箱
    pwd = request.POST.get('pwd')
    users = User.objects.filter(name=username)
    if users:   # 用户已存在
        return HttpResponse('wrong')
    # cap_old = request.session.ge  t('captcha')
    # if cap != cap_old:      #检查验证码
    #     return HttpResponse('wrong')
    pwd,salt = encrypt(pwd) #对密码进行加密
    try:
        with transaction.atomic():
            user = User.objects.create(name=username, password=pwd,salt=salt, email=username)   # 存储用户信息到数据库
            email_main(user)
    except:
        return HttpResponse('wrong')
    return HttpResponse('ok')


def encrypt(pwd,salt=None):
    '负责加密的函数'
    if salt is None:
        # 1.加盐加密
        l = '1234567890-=qwertyuiop[]asdfghjklzxcvbnm,./' # 做盐罐
        salt = ''.join(random.sample(l, 6))  # 随机取6粒盐
    pwd += salt
    # 2.哈希算法加密
    h = hashlib.md5()   # 创建哈希对象
    h.update(pwd.encode())  # 加载密码
    pwd = h.hexdigest() # 生成16进制密码
    return pwd,salt #返回加密后的密码和随机盐


def email_confirm(request):
    """
    渲染 邮箱确认 的页面
    :param request: 注册页面提交数据后跳转过来
    :return: 邮箱确认 页面
    """
    username=request.GET.get("username")
    return render(request,'userapp/email_confirm.html',{'username':username})


def regist_ok(request):
    username = request.GET.get('username')
    user = User.objects.filter(name=username)   # 查询到用户对象
    # 直接登录，保存登录状态&用户名&用户id
    request.session['login_state'] = 'ok'
    request.session['login_user'] = username
    request.session['login_userid'] = user[0].id
    return render(request, 'userapp/register ok.html',{'username':username,
                                                       'login_state': request.session.get('login_state'),
                                                       'login_user': request.session.get('login_user'),})


def login(request):
    '负责渲染login页面的函数'
    # 验证cookie，自动登陆
    username = request.COOKIES.get('username')
    pwd = request.COOKIES.get('password')
    user = User.objects.filter(name=username,password=pwd)
    if user:
        request.session['login_state'] = 'ok'
        request.session['login_user'] = username
        request.session['login_userid'] = user[0].id
        return redirect('mainapp:home')
    # cookie不存在或信息不符合，则只渲染login页面
    return render(request, 'userapp/login.html',{'login_state': request.session.get('login_state'),
                                                 'login_user': request.session.get('login_user'),})


def loginlogic(request):
    'ajax登陆请求的验证函数'
    #获取前端发来的相关参数
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    cap = request.POST.get('cap')
    remember = request.POST.get('remember')

    print(username,pwd,cap,remember)
    user = User.objects.filter(name=username)
    try:
        with transaction.atomic():
            print(user[0].has_confirm)
            if user[0].has_confirm:
                if user:
                    pwd = encrypt(pwd,user[0].salt)[0]  # 对pwd进行加密比对
                    if pwd == user[0].password:         #验证成功，保存登陆状态
                        request.session['login_state'] = 'ok'
                        request.session['login_user'] = username
                        request.session['login_userid'] = user[0].id
                        res = HttpResponse('ok')
                        if remember:    #勾选了记住我，则存储cookie
                            res.set_cookie('username',username,max_age=3600*24*7)
                            res.set_cookie('password', pwd,max_age=3600*24*7)
                        return res
            return HttpResponse('wrong')
    except:
        return HttpResponse('wrong')


def loginout(request):
    '登出函数'
    # 删除登陆状态&用户名&用户id
    del request.session['login_state']
    del request.session['login_user']
    del request.session['login_userid']
    res = redirect('userapp:after_user')
    #删除cookie记录的用户名和密码
    res.delete_cookie('username')
    res.delete_cookie('password')
    return res


def after_user(request):
    '登录或注册成功之后的跳转函数'
    #读出session中存储的路径信息，并重定向到相应路径
    path = request.session.get('path')
    return redirect(path)