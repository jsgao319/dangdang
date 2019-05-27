import datetime
import hashlib
import random
import time

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from mainapp.models import *
from .cart import *

##### 购物车相关函数 #####
def cart_add(request):
    '将订单项添加到购物车中'
    info_book = request.GET.get('book_id')
    info_amount = (int(request.GET.get('amount')) if request.GET.get('amount') else 1)
    print(info_book,info_amount)
    cart = request.session.get('cart')
    info = Info(Product.objects.get(id=info_book), info_amount) # 创建订单项对象
    if cart is None:    # 不存在则创建一个购物车
        cart = Cart()
    cart.add(info)      #将新建的订单项添加到购物车中
    request.session['cart'] = cart  #将购物车对象保存至session
    return HttpResponse('ok')

def cart_remove(request):
    '将订单项移入回收站'
    info_id = request.GET.get('info_id')
    cart = request.session.get('cart')
    cart.remove(info_id)
    request.session['cart'] = cart
    return HttpResponse('ok')

def cart_recover(request):
    '将回收站中的订单项恢复到购物车列表中'
    info_id = request.GET.get('info_id')
    cart = request.session.get('cart')
    cart.recover(info_id)
    request.session['cart'] = cart
    return HttpResponse('ok')

def cart_change_amount(request):
    '改变订单项中的数量'
    info_id = request.GET.get('info_id')
    new_amount = int(request.GET.get('new_amount'))
    cart = request.session.get('cart')
    cart.change_amount(info_id,new_amount)
    request.session['cart'] = cart
    return HttpResponse('ok')

def cart(request):
    '负责渲染购物车页面'
    dd_price = 0
    dd_amount = 0
    cart = request.session.get('cart')
    login_user = request.session.get('login_user')
    login_state = request.session.get('login_state')
    if cart:
        for info in cart.lst:
            if info.state == True:
                dd_price += info.amount * info.dangdang_price
                dd_amount  += info.amount
    return render(request, 'cartapp/car.html',{'cart':cart,'login_user':login_user,'login_state':login_state,'dd_price':dd_price,'dd_amount':dd_amount})



##### 订单相关函数 #####
def indent(request):
    '负责渲染订单页面'
    # 先判断登陆状态，若未登录则强制登陆
    if not request.session.get('login_state'):
        return redirect('userapp:login')
    # 处理订单创建失败后返回本页面的状态值
    order_fail = False
    if request.GET.get('order_fail') == 'True':
        order_fail = True
    # 获取用户的信息
    username = request.session.get('login_user')
    userid = request.session.get('login_userid')
    address = Address.objects.filter(user=userid)
    cart = request.session.get('cart')
    print('address:',address)
    return render(request, 'cartapp/indent.html',{'cart':cart,'address':address,'username':username,'order_fail':order_fail})


def pay_ok(request):

    # user = request.session.get('login_user')

    # if request.method == 'GET': # 筛去get请求
    #     return redirect('cartapp:indent')
    # 一、生成订单
    cart = request.session.get('cart')
    price = cart.dangdang_price
    login_userid = request.session.get('login_userid')
    user = User.objects.get(id=login_userid)
    username = user.name
    try:
        with transaction.atomic():
    # 生成地址表的条目
            addr = Address()
            addr.ship_man = request.POST.get('ship_man')
            addr.address = request.POST.get('address')
            addr.m_phone = request.POST.get('m_phone')
            addr.phone = request.POST.get('phone')
            addr.postcode = request.POST.get('postcode')
            addr.user = user
            addr.save()

            # 生成订单表的条目
                # 生成加密的订单号
            order_num = str(time.time())
                # 1.加盐加密
            l = '1234567890'  # 做盐罐
            salt = ''.join(random.sample(l, 6))  # 随机取6粒盐
            order_num += salt
                # 2.哈希算法加密
            h = hashlib.md5()  # 创建哈希对象
            h.update(order_num.encode())  # 加载密码
            order_num = h.hexdigest()  # 生成16进制密码
                # 创建订单
            order = Order.objects.create(number=order_num,user=user,address=addr,time=datetime.datetime.now())

            # 生成订单项表
            for info in cart.lst:   # 遍历，创建该订单中的所有订单项
                print(info)
                product = Product.objects.get(id=info.id)
                OrderInfo.objects.create(number=info.amount,order=order,product=product)
                if product:
                    cart.del1(info)
                    request.session['cart']=cart
    except:
        #重定向到订单页面，并附带fail的状态值
        url = reverse('cartapp:indent')
        url += '?order_fail=True'
        return redirect(url)
    return render(request,'cartapp/indent ok.html',{'user':username,'order_price':price})




