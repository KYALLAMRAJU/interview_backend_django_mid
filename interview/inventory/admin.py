from django.contrib import admin

from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "language"]
    list_filter = ["type", "language", "tags"]
    search_fields = ["name"]


@admin.register(InventoryTag)
class InventoryTagAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(InventoryLanguage)
class InventoryLanguageAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(InventoryType)
class InventoryTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
