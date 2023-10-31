import requests
import json
from comments import newsCountPerDay, getComment
from news.models import News
import os
from drf.local_settings import CLIENT_ID, CLIENT_SECRET

def get_token():
    url = 'https://api.aipaa.ir/auth/token/'  

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "client_id": CLIENT_ID,
        "client_secret":CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    jdata = json.dumps(data)
    response = requests.post(url, headers=headers, data=jdata)

    if response.status_code == 200:
        data = response.json()
        return(data['access_token'])
    else:
        print(f"Request failed with status code: {response.status_code}")


def call_tts(headline, guid, shamsi_pubDate, token):
    url = 'https://api.aipaa.ir/api/v1/voice/tts-file-response/?expire-file=yes' 

    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        "input_text": headline
    }

    jdata = json.dumps(data)
    response = requests.post(url, headers=headers, data=jdata)

    if response.status_code == 200:
        file_content = response.content

        base_directory = 'media/tts'
        variable_directory = os.path.join(base_directory, f"{shamsi_pubDate}")
        os.makedirs(variable_directory, exist_ok=True)
        file_path = os.path.join(variable_directory, f'{guid}.mp3')

        with open(file_path, 'wb') as file:
            file.write(file_content)
    else:
        print(f"Request failed with status code: {response.status_code}")


def main():
    token = get_token()
    queryset = News.objects.filter(tts_ready=False)

    for theNews in queryset:
        guid = theNews.guid
        data = getComment(guid)
        CountPerDay = dict()
        newsCountPerDay(data, CountPerDay)
        for val in CountPerDay.values():
            if val > 10:
                call_tts(theNews.headline, theNews.guid, theNews.shamsi_pubDate.date(), token)
                theNews.tts_ready =True
                theNews.save()
                break


if __name__ == "__main__":
    main()