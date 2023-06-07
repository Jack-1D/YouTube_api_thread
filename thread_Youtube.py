import threading
import requests
from pprint import pprint
from datetime import datetime
import time

info_list = []
YOUTUBE_API_KEY = "AIzaSyAwJPt6C1LMgVjXiLTVSB5Um7Qs_CDDp38"


def run(youtube_channel_id="UCjhwHd3mgmqm0ONm0bXKmng"):
    global info_list
    info_list.clear()
    start_time = time.time()

    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)

    
    threads = []
    video_ids = youtube_spider.get_playlist(uploads_id, max_results=50)
    print(video_ids)

    for video_id in video_ids:
        threads.append(threading.Thread(target = youtube_spider.get_video, args = (video_id,)))
    for i in range(len(video_ids)):
        threads[i].start()
    for i in range(len(video_ids)):
        threads[i].join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"共{len(video_ids)}部影片，花費{total_time}秒")
    for info in info_list:
        info['publishedAt'] = info['publishedAt'].strftime("%Y/%m/%d %H:%M:%S")
    return info_list, total_time


class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='contentDetails', max_results=10):
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.get_html_to_json(path)
        if not data:
            return []

        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids

    def get_video(self, video_id, part='snippet,statistics'):
        global info_list
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]

        try:
            time_ = datetime.strptime(data_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            time_ = None

        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {
            'id': data_item['id'],
            'channelTitle': data_item['snippet']['channelTitle'],
            'publishedAt': time_,
            'video_url': url_,
            'title': data_item['snippet']['title'],
            'description': data_item['snippet']['description'],
            'likeCount': data_item['statistics']['likeCount'],
            'commentCount': data_item['statistics']['commentCount'],
            'viewCount': data_item['statistics']['viewCount']
        }
        print(info)
        info_list.append(info)
        # return info

if __name__ == "__main__":
    run()