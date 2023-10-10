from rest_framework import serializers
from .models import News
import os
from django.conf import settings

class NewsByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'guid', 'pubDate', 'tts_ready')


class NewsSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField("get_categories")
    sub_categories = serializers.SerializerMethodField("get_sub_categories")
    download_link = serializers.SerializerMethodField("get_download_link")

    class Meta:
        model = News
        fields = ('title', 'comment_count', 'shamsi_pubDate', 'headline', 
                  'download_link', 'categories', 'sub_categories')

    def get_categories(self, obj):
        categories = obj.category.all()
        cats = list()

        for cat in categories:
            cats.append(cat.title)

        return cats
    
    def get_sub_categories(self, obj):
        sub_categories = obj.category.all()
        sub_cats = list()
        
        for cat in sub_categories:
            sub_cats.append(cat.title)

        return sub_cats
    
    def get_download_link(self, obj):
        if obj.tts_ready is False:
            return None

        request = self.context.get("request")
        file_path = f'tts/{obj.shamsi_pubDate.date()}/{obj.guid}.mp3'
        download_link = request.build_absolute_uri(settings.MEDIA_URL + file_path)
        
        return download_link 