from django.contrib import admin
from api.models import User, Goods, Order
# Register your models here.


class UserConfig(admin.ModelAdmin):
    list_display = ['user', 'password']
    list_select_related = True

    def patch_init(self,request,queryset):
        print(self, request, queryset)
        # queryset.update(date="1201xxxx")

    def patch_ret(self, request, queryset):
        pass
    patch_init.short_description = "初始化数据"
    patch_ret.short_description = "sssssss"

    actions = [patch_init, patch_ret]

    list_filter = ['user', 'password']


class GoodsConfig(admin.ModelAdmin):

    list_display = ['number', 'name', 'img', 'price', 'detail', 'count', 'startTime', 'endTime']

    list_display_links = ['number']

    list_filter = ['price']

    list_editable = ['price', 'count','startTime', 'endTime']

    search_fields = ['name', 'number']

    date_hierarchy = 'startTime'

    ordering = ['number']


class OrderConfig(admin.ModelAdmin):
    print(Order.objects.all())

    # list_display = ['user']

    list_filter = ['user__user', 'goods__name']

    readonly_fields = ['user', 'pay_count', 'goods']
    # filter_horizontal = ("goods",)

    # list_select_related = True
    # list_display_links = ['user']

    def patch_init(self,request,queryset):
        print(self, request, queryset)

    patch_init.short_description = "初始化数据."

# admin.site.register(models.User)
# admin.site.register(models.Goods)
# admin.site.register(models.Order)


admin.site.register(User, UserConfig)
admin.site.register(Goods, GoodsConfig)
admin.site.register(Order, OrderConfig)

admin.site.site_header = '商品后台系统'
admin.site.site_title = '商品后台系统'
