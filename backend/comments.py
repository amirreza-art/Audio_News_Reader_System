import requests
import os
import django
import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')
django.setup()
from news.models import News
from drf.local_settings import USER_AGENT

def newsCountPerDay(data_list, CountPerDay):
    for item in data_list:
        date = item.get("createDate", "")[:10]
        if date:
            if date in CountPerDay:
                CountPerDay[date] += 1
            else:
                CountPerDay[date] = 1

        if "children" in item:
            newsCountPerDay(item["children"], CountPerDay)


def getComment(guid):
    url = 'https://www.farsnews.ir/api/getcomments'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent' : USER_AGENT,
    }

    data = {
        'storyCode': f'{guid}'
    }

    for _ in range(3):
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return data
        time.sleep(5)
        
    print(guid)
    return []


def newsCount(data):
    count = 0

    if isinstance(data, dict):
        if "id" in data:
            count += 1
        for value in data.values():
            count += newsCount(value)

    elif isinstance(data, list):
        for item in data:
            count += newsCount(item)

    return count


def setCommentsCount(queryset):
    for theNews in queryset:
        try:
            count = newsCount(getComment(theNews.guid))
            if count > theNews.comment_count:
                theNews.comment_count = count
                theNews.save()
        except Exception:
            continue


if __name__ == "__main__":
    queryset = News.objects.all()
    setCommentsCount(queryset)
