import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler


client_id = 'b4a9560bab83459a923eeee6801e9f93'
client_secret = '398b2d7c3d764ef2a6000f55037938a4'

# Spotipyを初期化
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# データの読み込み
tiktok_data = pd.read_csv('tiktok_data.csv')
not_tiktok_data = pd.read_csv('not_tiktok_data.csv')

# データセットの結合とラベル付け
tiktok_data['Label'] = 1
not_tiktok_data['Label'] = 0
dataset = pd.concat([tiktok_data, not_tiktok_data])
x = dataset[['ダンスに適しているか', 'エネルギーの強さ']]
y = dataset['Label']

# データの標準化
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# モデルの読み込み
loaded_model = load('model.joblib')

# 予測
def predict_tiktok_song(song_features):
    song_features_scaled = scaler.transform([song_features])
    prediction = loaded_model.predict(song_features_scaled)
    if prediction[0] == 1:
        return "この曲はtiktokで\"使われる\"可能性の高い曲です。"
    else:
        return "この曲はtiktokで\"使われない\"可能性の高い曲です。"

# 曲のIDを入力
track_id = input("判別したい曲のIDを入力してください: ")  # 例：4fMewVWtew1oB6d3E8x9pp, 06XQvnJb53SUYmlWIhUXUi

# danceabilityとenergyを取得
audio_features = sp.audio_features(track_id)[0]
danceability = audio_features['danceability']
energy = audio_features['energy']

# 曲の特徴量を与えて判別する
song_features = [danceability, energy]
prediction_result = predict_tiktok_song(song_features)
print(prediction_result)
