"""
微博登录
"""
# 获取code
def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_weibo_url = "http://127.0.0.1:8000/login/check/"
    qq_auth_url = "https://"
    auth_url = "https://api.weibo.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id="3214515364", redirect_uri=redirect_weibo_url)
    print(auth_url)


# 得到access_token
def request_token_message():
    import requests
    client_id = 3214515364
    client_secret = "1b9b415350019674abfda80d0ef24cca"
    grant_type = ""
    redirect_uri = "http://127.0.0.1:8000/login/check/"
    code = "88cfffece305b7577a12cc8419bb0612"
    get_Access_token_url = "https://api.weibo.com/oauth2/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}".format(client_id, client_secret, redirect_uri, code)
    response = requests.post(url=get_Access_token_url)
    print(response.text)


# 得到个人信息
def get_message():
    import requests
    access_token = {"access_token": "2.007NjOZGASmXVDaa7e701dc0bJCadC", "remind_in": "157679999", "expires_in": 157679999, "uid": "6017479156", "isRealName": "true"}
    access_token = "2.007NjOZGASmXVDaa7e701dc0bJCadC"
    redirect_uri = "http://127.0.0.1:8080/home"
    uid = 6017479156
    get_message_url = "https://api.weibo.com/2/users/show.json?access_token={}&uid={}&redirect_uri={}".format(access_token, uid, redirect_uri)
    response = requests.get(url=get_message_url)
    r = response.text
    print(r)


if __name__ == '__main__':
    # get_auth_url()
    # request_token_message()
    get_message()