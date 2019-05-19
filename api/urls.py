from django.conf.urls import url
from api.views import login, list, message

urlpatterns = [
    url(r'^login/geturl/$', login.GetUrl.as_view()),
    url(r'^login/$', login.AuthView.as_view()),
    url(r'^list/$', list.ListView.as_view({'get': 'list'})),
    url('^message/$', message.MessageView.as_view({'post': 'message'})),
    url('^add/$', message.MessageView.as_view({'post': 'add'}))
]