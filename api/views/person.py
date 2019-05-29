from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from ..models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    # pay_count = serializers.CharField(source='goods.number', read_only=True)
    # name = serializers.CharField(source='goods.name', read_only=True)
    # img = serializers.CharField(source='goods.img', read_only=True)
    # price = serializers.CharField(source='goods.price', read_only=True)
    # detail = serializers.CharField(source='goods.detail', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'pay_count', 'goods']
        depth = 1
        # exclude = ['user']  # 去除某个字段


class PersonView(ViewSetMixin, APIView):
    def person(self, request, *args, **kwargs):
        data = request.data
        print(data)
        ret = {}
        user = data['username']
        if not user:
            ret['code'] = 1002
            ret['error'] = "拒绝访问"
            return Response(ret)
        queryset = Order.objects.filter(user__user=user)
        serializers_order = OrderSerializer(instance=queryset, many=True)
        ret['data'] = serializers_order.data
        
        return Response(ret)
