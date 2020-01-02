from django.contrib import admin
#from django.http import HttpResponse
#from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.admin.models import LogEntry
from blog_sys.base_admin import BaseOwnerAdmin
from blog.adminforms import PostAdminForm
from blog_sys.custom_site import custom_site
from .models import Post,Category,Tag
#from django.contrib.auth import get_permission_codename
# Register your models here.


class PostInline(admin.TabularInline):
    fields =('title','desc')
    extra = 1
    model = Post


@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status',  'created_time')
    fields = ('name', 'status')

#PERMISSION_API= "https://permission.sso.com/has_perm?user={}&perm_code={}"


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id =self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form =PostAdminForm
    list_display = [
        'title','category','status','created_time','operator','owner'
    ]
    list_display_links = []

    list_filter = ['category',]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    exclude = ('owner',)
    fieldsets = (
        ('基础配置',{'description':'基础配置描述','fields':(('title','category'),'status',)}),
        ('内容',{'fields':('desc','content',),}),
        ('额外信息',{'classes':('wide',),'fields':('tag',),})

    )
    filter_vertical = ('tag',)

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id ,))
        )
    operator.short_description = '操作'


    class Media:
        css ={
            'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js =('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bubdle.js',)

@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']

"""  def has_add_permission(self, request):
        opts =self.opts
        codename =get_permission_codename('add',opts)
        perm_code="%s.%s"%(opts.app_label,codename)
        resp=request.get(PERMISSION_API.format(request.user.username,perm_code))
        if resp.status_code == 200:
            return True
        else:
            return False"""



