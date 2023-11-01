from comments import setCommentsCount
import datetime
from news.models import News
import schedule
import time


def my_task():
    print(f"starttttt...========================={datetime.datetime.now()}")
    queryset = News.objects.filter(miladi_pubDate__date=datetime.datetime.now().date())
    setCommentsCount(queryset)
    print(f"enddddddd...========================={datetime.datetime.now()}")


schedule.every(10).minutes.do(my_task)

while True:
    schedule.run_pending()
    time.sleep(1)