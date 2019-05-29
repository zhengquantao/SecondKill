from django.conf.urls import url
from api.views import login, list, message, person, pay

urlpatterns = [
    url(r'^login/geturl/$', login.GetUrl.as_view()),
    url(r'^login/$', login.AuthView.as_view()),
    url(r'^list/$', list.ListView.as_view({'get': 'list'})),
    url('^message/$', message.MessageView.as_view({'post': 'message'})),
    url('^add/$', message.MessageView.as_view({'post': 'add'})),
    url('^person/$', person.PersonView.as_view({'post': "person"})),
    url('^pay/alipay/$', pay.AlipayView.as_view({'post': 'alipay'})),
    url('^update_order/$', pay.AlipayView.as_view({'post': 'update_order'}))
]