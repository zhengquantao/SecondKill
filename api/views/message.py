from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from ..models import Goods
from ..utils.redis_server import redis_server
from .list import GoodsSerializer
from ast import literal_eval
from ..utils.activeMQ import send_to_queue, receive_from_queue

import time


class MessageView(ViewSetMixin, APIView):
    def add(self, request, *args, **kwargs):
        goods_list = Goods.objects.all()
        for good in goods_list:
            redis_server().set(good.number, good.count, 60*60*2)
            # redis_server().set(good.number, good.count)
        
        return Response({})

    def message(self, request, *args, **kwargs):
        data = request.data
        print(data)

        ret = {"code": 1000}
        if not data:
            return Response({})
        # 先查询是否存在这个用户
        check_data = cache.get(data['username'])
        if not check_data:
            ret["code"] = 1001
            ret["error"] = "禁止访问"
            return Response(ret)
        # 在查询id是否被禁止
        # check_data = literal_eval(redis_server().get(data['username']).decode("utf-8"))
        
        if check_data[1] != data['token'] or check_data[2] == 0:
            print(check_data[2] == 0, '======')
            ret["code"] = 1001
            ret["error"] = "禁止访问"
            return Response(ret)
        # 固定窗口计数 限流
        # 计数
        counts = redis_server().incrby(data['username']+'s', 1)
        if counts == 1:
            # 设置超时时间
            redis_server().expire(data['username']+'s', 10)
        if counts > 5:
            check_data[2] = 0
            cache.set(data['username'], check_data, 60*60)
            ret["code"] = 1001
            ret["error"] = "禁止访问"
            return Response(ret)

        # # 把消息放入到队列之中
        # send_to_queue(str(data))
        # # 取出来
        # # receive_data = receive_from_queue()

        # 事务
        count = redis_server().get(data['number'])

        # 开启原子操作
        pipe = redis_server().pipeline(transaction=True)

        #  监视数据是否发送改变
        pipe.watch(data['number'])

        # 确认 key 有没有
        if not pipe.exists(data['number']):
            pipe.set(data['number'], count)
            pipe.execute()

        # 事务开始
        if int(pipe.get(data['number']).decode('utf-8')) > 0:
            try:
                pipe.multi()
                pipe.decr(data['number'])
                # 提交事务
                count_now = pipe.execute()[0]
                print(count_now)
                Goods.objects.filter(number=data['number']).update(count=count_now)
                # 更改redis数量
                # redis_server().set(data['number'], count_now)
                ret['count'] = count_now
                new_queryset = Goods.objects.all()
                # 更改redis总体数据
                serializers_goods = GoodsSerializer(instance=new_queryset, many=True)
                for item in serializers_goods.data:
                    start_time = time.strptime(item['startTime'], '%Y-%m-%d %H:%M:%S')
                    end_time = time.strptime(item['endTime'], '%Y-%m-%d %H:%M:%S')
                    item['startTime'] = time.mktime(start_time)  # 开始时间
                    item['endTime'] = time.mktime(end_time)  # 结束时间
                cache.set("Kill", serializers_goods.data, 60 * 5)
            except Exception as e:
                print(e, '0000000')

        else:

            ret['code'] = 1001
            ret['error'] = "秒杀失败"

        return Response(ret)