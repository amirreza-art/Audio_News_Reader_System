from rest_framework import serializers
from .models import News

class NewsByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'guid', 'pubDate', 'tts_ready')
