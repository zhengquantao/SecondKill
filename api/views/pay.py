from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from api.utils.pay import AliPay
from django.conf import settings
from django.core.cache import cache
import time
from api.models import Order


def aliPay():
    obj = AliPay(
        appid=settings.APPID,
        app_notify_url=settings.NOTIFY_URL,  # 如果支付成功， 支付宝想这个地址发送POST请求（效验是否支付已经完成）
        return_url=settings.RETURN_URL,  # 如果支付成功， 重定向到你的网站位置
        alipay_public_key_path=settings.PUB_KEY_PATH,  # 支付宝公钥
        app_private_key_path=settings.PRI_KEY_PATH,  # app应用私钥
        debug=True,  # 默认False
    )
    return obj


class AlipayView(ViewSetMixin, APIView):
    def alipay(self, request, *args, **kwargs):
        data = request.data
        ret = {}
        if not data:
            ret['code'] = 1001
            return Response(ret)
        if not cache.get(data['username']):
            ret['code'] = 1001
            return Response(ret)
        print(data)
        alipay = aliPay()  # 调用上面的信息

        price = float(data['price'])
        out_trade_no = "x2" + str(time.time())
        cache.set(out_trade_no, data['id'], 60*60*30)
        # 价格，购买的商品加密
        # 拼接成URL
        query_params = alipay.direct_pay(
            subject=data['goodName'],  # 商品简单描述
            out_trade_no=out_trade_no,  # 商户订单号
            total_amount=price,  # 交易金额（单位: 元 保留两位小数）
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        ret['code'] = 1000
        ret['url'] = pay_url
        return Response(ret)


    def update_order(self, request, *args, **kwargs):
        data = request.data
        print(data)
        from urllib.parse import parse_qs

        body_srt = request.body.decode('utf-8')
        post_data = parse_qs(body_srt)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            print(out_trade_no)
            good_id = cache.get(out_trade_no)
            Order.objects.filter(id=good_id).update(pay_count=1)
            # 2. 根据订单号将数据库中的数据进行更新
            ret = {"status": '支付成功'}
            return Response(ret)
        else:
            ret = {"status": '支付失败'}
            return Response(ret)

