from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
import re

class ForceLogin(MiddlewareMixin):
    def process_response(self, request, response):
        path = request.path
        print('---------中间件-----------',path)
        # useful_path = ['^/mian/home','^/mian/booklist/','^/mian/home']
        path = request.path     #每次请求的路径
        if re.findall('^/main/',path) or re.findall('^/cart/',path) :     #当为其他模块的请求时，记录路径
            print('备选的path----------',request.path)
            request.session['path'] = request.path
        return response  # 必须返回response