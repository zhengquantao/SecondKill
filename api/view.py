"""
微博登录
"""

from django.shortcuts import render, redirect
from api.models import UserToken, User
from django.utils.http import is_safe_url
from .utils.login_key import weibo, qq, weixin
import uuid
import json
import requests


def proxy_login_weibo(request):
    code = request.GET.get('code')
    client_id, client_secret = weibo()
    # 请求得到access_token
    redirect_uri = "http://127.0.0.1:8000/login/weibo/"
    get_Access_token_url = "https://api.weibo.com/oauth2/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}".format(
        client_id, client_secret, redirect_uri, code)
    response = requests.post(url=get_Access_token_url).text
    response_loads = json.loads(response)
    print(response_loads)
    access_token = response_loads['access_token']
    print(access_token)
    uid = response_loads['uid']
    # 请求得到用户信息
    get_message_url = "https://api.weibo.com/2/users/show.json?access_token={}&uid={}&redirect_uri={}".format(
        access_token, uid, redirect_uri)
    info_message = requests.get(url=get_message_url).text
    info_message_loads = json.loads(info_message)
    user = info_message_loads['name']
    # 存入数据库
    is_user = User.objects.filter(user=user)
    if is_user:

        token = str(uuid.uuid4())
        is_user.update(password=token)
    else:
        token = str(uuid.uuid4())
        User.objects.create(user=is_user, password=token)

    # 拿到请求路径
    # path = request.get_host()
    # print(is_safe_url("http://127.0.0.1:8080/home", allowed_hosts={"127.0.0.1:8080"}))
    redirect_url = redirect("http://127.0.0.1:8080/home/")
    redirect_url.set_cookie("name", user.encode('utf-8').decode('latin-1'))
    redirect_url.set_cookie("token", token)

    return redirect_url


def proxy_login_qq(request):
    code = request.GET.get('code')
    client_id, client_secret = qq()
    # 请求得到access_token
    redirect_uri = "http://127.0.0.1:8000/login/qq"
    get_Access_token_url = "https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id={}&client_secret={}&redirect_uri={}&code={}".format(
        client_id, client_secret, redirect_uri, code)
    response = requests.get(url=get_Access_token_url).text
    print(response)
    # FFFB91C30F6F87EA5BF9570AEC2E23F & expires_in = 7776000 & refresh_token = 7
    # F135B51779C7595DED58D85C87419CE
    # print(access_token)
    access_token = response.split('&')[0]
    access_token = access_token[13:]

    # 获取openid
    get_open_id_url = "https://graph.qq.com/oauth2.0/me?access_token={}".format(access_token)
    response_open_id = requests.get(url=get_open_id_url).text
    # print(response_open_id)
    # callback({"client_id": "101576925", "openid": "B3F2C9D7A081D39936017FF97166052A"});
    response_open_id_dict = eval(response_open_id[9:-3])
    open_id = response_open_id_dict.get('openid')
    # 获取个人信息
    get_user_info_url = "https://graph.qq.com/user/get_user_info?access_token={}&oauth_consumer_key={}&openid={}".format(
        access_token, client_id, open_id
    )

    response_user_info = requests.get(url=get_user_info_url).text
    response_user_info = json.loads(response_user_info)
    user = response_user_info['nickname']

    # 存入数据库
    is_user = User.objects.filter(user=user)
    if is_user:
        token = str(uuid.uuid4())
        is_user.update(password=token)
    else:
        token = str(uuid.uuid4())
        User.objects.create(user=user, password=token)

    # 拿到请求路径
    # path = request.get_host()
    # print(is_safe_url("http://127.0.0.1:8080/home", allowed_hosts={"127.0.0.1:8080"}))
    redirect_url = redirect("http://127.0.0.1:8080/home/")
    redirect_url.set_cookie("name", user.encode('utf-8').decode('latin-1'))
    redirect_url.set_cookie("token", token)

    return redirect_url


def proxy_login_weixin(request):
    pass

