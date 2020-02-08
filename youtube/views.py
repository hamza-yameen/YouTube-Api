from django.shortcuts import render, redirect
from django.conf import settings
import requests
from isodate import parse_duration


def home(request):

    ved_detail = []

    if request.method == 'POST':

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        r = requests.get(search_url, params=params)
        result = r.json()['items']

        v_ids = []
        for res in result:
            v_ids.append(res['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ v_ids[0] }')

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(v_ids)
        }

        r = requests.get(video_url, params=video_params)
        result = r.json()['items']

        for ved_res in result:
            v_data = {
                'title': ved_res['snippet']['title'],
                'id': ved_res['id'],
                'url': f'https://www.youtube.com/watch?v={ ved_res["id"] }',
                'duration': parse_duration(ved_res['contentDetails']['duration']).total_seconds() // 60,
                'thumbnail': ved_res['snippet']['thumbnails']['high']['url']
            }
            ved_detail.append(v_data)

    context = {
        'videos': ved_detail
    }

    return render(request, 'Home.html', context)
