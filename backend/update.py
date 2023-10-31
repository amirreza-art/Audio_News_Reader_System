from comments import setCommentsCount
from news.models import News


def updateHeadAndTitle():
    from bs4 import BeautifulSoup
    import requests

    queryset = News.objects.all()
    
    for item in queryset:
        url = item.link
        response = requests.get(url)
        html_content = response.text
        sub_soup = BeautifulSoup(html_content, 'html.parser')

        try:
            title = sub_soup.find('h1', class_='title').text.strip()   
        except Exception:
            try: 
                title = sub_soup.find('span', class_='title').text.strip() 
            except Exception: 
                continue

        try:
            head = sub_soup.find('p', class_='lead').text.strip()   
        except Exception:
            try: 
                head = sub_soup.find('span', class_='lead').text.strip() 
            except Exception: 
                continue
        
        item.title = title
        item.headline = head
        item.save()


if __name__ == "__main__":
    # updateHeadAndTitle()
    pass