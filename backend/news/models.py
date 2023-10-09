from django.db import models
from persiantools.jdatetime import JalaliDateTime
import datetime


class Category(models.Model):
    title = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.title
    

class SubCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")
    
    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=150)
    link = models.URLField()
    guid = models.BigIntegerField(unique=True)
    headline = models.TextField()
    comment_count = models.IntegerField(default=0)
    tts_ready = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pubDate = models.CharField(max_length=50)
    shamsi_pubDate = models.DateTimeField(blank=True, null=True)
    miladi_pubDate = models.DateTimeField(blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='news_items')
    sub_category = models.ManyToManyField(SubCategory, related_name='news_items')

    def convert_to_shamsi(self):
        parsed_datetime = datetime.datetime.strptime(self.pubDate, "%a, %d %b %Y %H:%M:%S %Z")
        shamsi_pubDate = JalaliDateTime.to_jalali(parsed_datetime)
        self.shamsi_pubDate = shamsi_pubDate.strftime("%Y-%m-%d %H:%M:%S")

    def convert_to_miladi(self):
        parsed_datetime = datetime.datetime.strptime(self.pubDate, "%a, %d %b %Y %H:%M:%S %Z")
        self.miladi_pubDate = parsed_datetime

    def save(self, *args, **kwargs):
        if self.pubDate and not self.shamsi_pubDate:
            self.convert_to_shamsi()
        if self.pubDate and not self.miladi_pubDate:
            self.convert_to_miladi()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guid} : {self.title}"