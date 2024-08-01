from requests import post, get
import os
import base64
from dotenv import load_dotenv
import json
from pytube import YouTube

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result =  json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization":"Bearer " + token}

def get_playlist(token, playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?market=US'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def startDownload(id):
    try:
        default_url = 'https://www.youtube.com/watch?v='
        id = id
        ytLink = default_url + id
        ytObject = YouTube(ytLink)
        video = ytObject.streams.get_audio_only()
        video.download()
    except:
        print("Youtube link is invalid")
    print("Download Complete...")


playlist_id = input("What is your playlist id? ")
token = get_token()

search = get_playlist(token, playlist_id)
music_list = []
for item in search:
    music_list.append(item['track']['name'])
    print(item['track']['name'])

api_key = 'AIzaSyAFmb5Dj0p4a9UwxQYUB6n7Zu0He79XV4U'
youtube_url = "https://www.googleapis.com/youtube/v3/search"
video_ids = []
for name in music_list:
    search_query = name
    query = f"?part=snippet&q={search_query}&type=video&key={api_key}"
    final_url = youtube_url + query
    response = get(final_url)
    json_data = json.loads(response.content)['items']
    print(json_data[0]['id']['videoId'])
    video_ids.append(json_data[0]['id']['videoId'])

for i in video_ids:
    startDownload(i)
