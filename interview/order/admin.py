from django.contrib import admin

from interview.order.models import Order, OrderTag


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["inventory", "start_date", "embargo_date", "is_active"]
    list_filter = ["is_active", "tags"]
    search_fields = ["inventory__name"]


@admin.register(OrderTag)
class OrderTagAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
