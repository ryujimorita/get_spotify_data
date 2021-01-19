# colabの環境にspotipyをインストール
!pip install spotipy

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# spotify developerから取得したclient_idとclient_secretを入力
client_id = '〇〇〇'
client_secret = '△△△'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

# Spotifyのユーザー名と、プレイリストのIDを入力
ids = getTrackIDs('username', 'playlist_id')

# データの確認
# print(len(ids))
# print(ids)

# 楽曲のメタデータの取得する関数の定義
def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    mode = features[0]['mode']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']

    track = [name, album, artist, release_date, length, mode, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
    return track


# 全トラックIDにうえで定義したメタデータ取得関数をループさせる
tracks = []
for i in range(len(ids)):
    time.sleep(.5)
    track = getTrackFeatures(ids[i])
    tracks.append(track)

# データセットの作成
df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'mode', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence'])

df.head()

# データのCSV書き出し、ローカルからダウンロード
df.to_csv("spotify_utada_songdata.csv", sep = ',')
from google.colab import files
files.download('spotify_utada_songdata.csv')
