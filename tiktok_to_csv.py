import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

# SpotifyのクライアントIDとシークレットを設定
client_id = 'b4a9560bab83459a923eeee6801e9f93'
client_secret = '398b2d7c3d764ef2a6000f55037938a4'

# Spotipyを初期化
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# プレイリストIDのリスト
playlist_ids = ['6aiVSJxdJNAitWYUX9COf7',  # 検索上位8件
                '3QYMGj323cdr59m6FM67Cw',
                '5vsKp4Ihj3DHr63lIAHAnU',
                '3Xe3FgADaMb06zRGAWmhox',
                '3WJTxB4dXK3zF3ogW5HWgy',
                '4IrP3zdH9dGMfIFibCJsIc',
                '3y6tKgCW3miL0BlFsXvY73',
                '4EEF57Ds5UbIKetdC8X9ne',
                '1Q60eGVbKObfl7MRDjWu9C',
                '4c2YWOkIft7WdP07KNjNgG']

# 出力ファイル名
output_file = 'tiktok_data.csv'

# 取得するデータのヘッダー
header = ['ID', '曲名', '作曲者', '音響的な特徴', 'ダンスに適しているか', 'エネルギーの強さ', 'インストゥルメンタルか', 'キー',
        'ライブ録音か', '音量', 'モード', '音声の存在', 'テンポ（BPM）', '拍子記号', '再生時間（ms）', 'ポジティブさ']

# トラック情報を格納するリスト
track_data = []

# プレイリストごとにトラック情報を取得
for playlist_id in playlist_ids:
    # プレイリストのトラック情報を取得
    results = sp.playlist_tracks(playlist_id, fields='items(track(id,name,artists(name))),total')
    total_tracks = results['total']

    # ページングを考慮してすべてのトラック情報を取得
    offset = 0
    while offset < total_tracks:
        results = sp.playlist_tracks(playlist_id, fields='items(track(id,name,artists(name))),total', offset=offset)
        tracks = results['items']
        for track in tracks:
            track_id = track['track']['id']
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            track_data.append([track_id, track_name, artist_name])
        offset += len(tracks)

# 重複をなくすためにtrack_idとtrack_nameのセットを作成し、重複のないトラック情報を抽出
unique_track_data = []
existing_ids = set()
existing_names = set()

for track_info in track_data:
    track_id = track_info[0]
    track_name = track_info[1]
    if track_id not in existing_ids and track_name not in existing_names:
        unique_track_data.append(track_info)
        existing_ids.add(track_id)
        existing_names.add(track_name)

# 取得した曲データに対してAudio Featuresを取得
for i in range(len(unique_track_data)):
    track_id = unique_track_data[i][0]
    features = sp.audio_features(track_id)[0]
    unique_track_data[i].extend([features['acousticness'], features['danceability'], features['energy'],
                                features['instrumentalness'], features['key'], features['liveness'],
                                features['loudness'], features['mode'], features['speechiness'],
                                features['tempo'], features['time_signature'], features['duration_ms'],
                                features['valence']])

# データをcsvファイルに書き出す
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(unique_track_data)

print('データの書き出しを完了しました。')
