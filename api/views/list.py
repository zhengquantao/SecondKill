from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from api.models import Goods
import time
from ..utils.redis_server import redis_server
from rest_framework.viewsets import GenericViewSet, ViewSetMixin


class GoodsSerializer(serializers.ModelSerializer):
    startTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    endTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Goods
        fields = ['number', 'name', 'img', 'price', 'detail', 'count', 'startTime', 'endTime']   # 查询全部 '__all__'
        # depth = 2  # 根据关联字段找到表序列化2层（0-10）
        # exclude = ('add_time',):  除去指定的某些字段


class ListView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        goods_kill = cache.get("Kill")
        print(goods_kill)
        if goods_kill:
            ret["data"] = goods_kill
            return Response(ret)
        else:
            try:
                queryset = Goods.objects.all()
                serializers_goods = GoodsSerializer(instance=queryset, many=True)
                for item in serializers_goods.data:
                    start_time = time.strptime(item['startTime'], '%Y-%m-%d %H:%M:%S')
                    end_time = time.strptime(item['endTime'], '%Y-%m-%d %H:%M:%S')
                    item['startTime'] = time.mktime(start_time)  # 开始时间
                    item['endTime'] = time.mktime(end_time)  # 结束时间

                ret["data"] = serializers_goods.data
                cache.set("Kill", serializers_goods.data, 60*5)
            except:
                ret["code"] = 1001
                ret["error"] = "获取失败"
            return Response(ret)