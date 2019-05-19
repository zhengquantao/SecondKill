from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils.login_key import weibo
from ..utils.redis_server import redis_server
from ast import literal_eval  # 将字符串转成字典
from api.models import User
import uuid


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data.get('username'))
        ret = {'code': 1000}
        username = request.data.get('username')
        password = request.data.get('password')
        # 查缓存 解码 转成字典
        # exists_user = literal_eval(redis_server().get(username).decode("utf-8"))
        
        exists_user = cache.get(username)
        if exists_user and exists_user[0] == password and exists_user[2] != 0:
            ret['token'] = exists_user[1]
            return Response(ret)
        # 可以去掉
        else:
            user = User.objects.filter(user=username, password=password).filter()
            if not user:
                ret['code'] = 1001
                ret['error'] = "用户名密码错误"
            else:
                # 存在 直接存入缓存之中(密码, token, 登入状态)
                uid = str(uuid.uuid4())
                ret['token'] = uid
                # redis_server().set(username, [password, uid, 1], 60*60*6)
                cache.set(username, [password, uid, 1], 60*60*6)
        return Response(ret)


class GetUrl(APIView):

    def post(self, request, *args, **kwargs):
        # weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
        redirect_weibo_url = "http://127.0.0.1:8000/login/weibo/"
        client_id, client_secret = weibo()
        auth_url = "https://api.weibo.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}".format(
            client_id=client_id, redirect_uri=redirect_weibo_url)
        ret = {"urls": auth_url}
        # print(auth_url)
        return Response(ret)


class GetMessage(APIView):
    def get(self, request, *args, **kwarts):
        code = request.data.get('code')
        import requests
        client_id = 3214515364
        client_secret = "1b9b415350019674abfda80d0ef24cca"
        redirect_uri = "http://127.0.0.1:8080/home"
        # code = "88cfffece305b7577a12cc8419bb0612"
        get_Access_token_url = "https://api.weibo.com/oauth2/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}".format(
            client_id, client_secret, redirect_uri, code)
        response = requests.post(url=get_Access_token_url)
        print(response.text)
        return Response()
