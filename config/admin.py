from django.contrib import admin

from base_admin import BaseOwnerAdmin
from custom_site import custom_site
from .models import Link,SideBar
# Register your models here.

@admin.register(Link,site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title','href','status','weight','created_time')
    fields = ('title','href','status','weight')


@admin.register(SideBar,site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content','created_time')
    fields = ('title',  'display_type', 'content')
