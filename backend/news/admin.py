from django.contrib import admin
from django.contrib.admin import register
from .models import Category, SubCategory, News

# Register your models here.
@register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('guid', 'comment_count', 'title', 'tts_ready', 'display_categories', 'display_subcategories',)
    list_filter = ('tts_ready',)
    search_fields = ('guid',)
    
    def display_subcategories(self, obj):
        return "---".join([subcategory.title for subcategory in obj.sub_category.all()])

    display_subcategories.short_description = 'SubCats'

    def display_categories(self, obj):
        return "---".join([category.title for category in obj.category.all()])

    display_categories.short_description = 'Categories'


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id',)


@register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id',)
