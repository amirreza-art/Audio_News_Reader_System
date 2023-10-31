import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from lxml import etree
import os
import django
from comments import getComment, newsCount

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')
django.setup()
from news.models import Category, SubCategory, News


def removeExtraSpaces(text):
    result = re.sub(r'\s+', ' ', text).strip()
    return result
            

def createTheNews(complete_url, category, subcat):
    response = requests.get(complete_url)
    sub_html_content = response.content
    elem = etree.fromstring(sub_html_content)

    links = elem.findall('channel/item/link')
    titles = elem.findall('channel/item/title')
    guids = elem.findall('channel/item/guid')
    pubDates = elem.findall('channel/item/pubDate')
    
    for i in range(len(links)):
        sub_url = links[i].text.strip()
        sub_response = requests.get(sub_url)
        sub_html_content = sub_response.content
        sub_soup = BeautifulSoup(sub_html_content, 'html.parser')
        try:
            head = sub_soup.find('p', class_='lead').text.strip()   
        except Exception:
            try:
                head = sub_soup.find('span', class_='lead').text.strip() 
            except Exception: 
                continue
        
        guid = int(re.search(r"\d+", guids[i].text.strip()).group())
        try:
            comment_count = newsCount(getComment(guid))
        except Exception:
            comment_count = 0

        news, created = News.objects.get_or_create(guid=guid, defaults={
                                                            'title': titles[i].text.strip(),
                                                            'link': sub_url,
                                                            'headline': head,
                                                            'pubDate': pubDates[i].text,
                                                            'comment_count': comment_count,
                                                            })
        news.category.add(category)
        news.sub_category.add(subcat)

        if created:
            news.save()



def main():
    url = "https://www.farsnews.ir/rsslinks"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    a_elements = soup.find_all('a')
    for a_element in a_elements:
        try:
            href = a_element.get('href')

            if not (href and href.startswith('/rss')):
                continue

            complete_url = urljoin(url, href)
            text = a_element.text.strip()
            subcat_title = removeExtraSpaces(text)
            keyword = "آخرین اخبار"
            match = re.search(rf"{re.escape(keyword)}(.*)", text)

            if match:
                subtext = match.group(1).strip()
                category_title = removeExtraSpaces(subtext)

            category, created = Category.objects.get_or_create(title=category_title)
            if created:
                category.save()
            
            subcat, created = SubCategory.objects.get_or_create(title=subcat_title, defaults={'category_id': category.id,})
            if created:
                subcat.save()
            
            createTheNews(complete_url, category, subcat)  
        except:
            continue


if __name__ == "__main__":
    main()
