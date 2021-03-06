"""SecondKill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api import view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>\w+)/', include('api.urls')),
    # 自己写的
    url(r'^login/weibo/', view.proxy_login_weibo),
    url(r'^login/qq$', view.proxy_login_qq),
    url(r'^login/weixin/', view.proxy_login_weixin),
    url(r'^update_order', view.update_order),
    # 第三方登录组件
    url('', include('social_django.urls', namespace='social'))
]