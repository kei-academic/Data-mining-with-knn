import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import itertools
from joblib import dump
from tabulate import tabulate


# データの読み込み
tiktok_data = pd.read_csv('tiktok_data.csv')
not_tiktok_data = pd.read_csv('not_tiktok_data.csv')

# データセットの結合とラベル付け
tiktok_data['Label'] = 1  # tiktokで使われる曲はラベル1
not_tiktok_data['Label'] = 0  # tiktokで使われない曲はラベル0
dataset = pd.concat([tiktok_data, not_tiktok_data], ignore_index=True)

# 扱う説明変数の組み合わせを列挙
variables = ['音響的な特徴', 'ダンスに適しているか', 'エネルギーの強さ', 'インストゥルメンタルか',
            'キー', 'モード', 'テンポ（BPM）', 'ポジティブさ']
combinations = list(itertools.combinations(variables, 2))

# 最適なkと評価値を保存するためのリスト
scores = []

for feature1, feature2 in combinations:
    x = dataset[[feature1, feature2]]
    y = dataset['Label']

    # データの標準化
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)  # 特徴量の比率を揃える

    # 訓練データとテストデータへの分割
    x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=41)  # テスト用は20%、シード値は41(適当)

    # 最適なkの値を探す
    list_nn = []
    list_score = []
    for k in range(1, 31):  # k = 1~30
        knc = KNeighborsClassifier(n_neighbors=k)
        knc.fit(x_train, y_train)  # xは特徴量データ、yは訓練データ

        # 評価
        score = knc.score(x_test, y_test)
        # k=1~30の詳細表示
        # print("{} score: {:.4f}".format(k, score))

        list_nn.append(k)
        list_score.append(score)

    best_score = max(list_score)
    best_k = list_nn[list_score.index(best_score)]
    scores.append((feature1, feature2, best_k, best_score))
    # 各組み合わせにおける最適なkと評価値を表示
    # print("組み合わせ：{}".format([feature1, feature2]))
    # print("最高精度：k={}のとき{:.4f}％".format(best_k, max(list_score)*100))

    # プロット
    # if [feature1, feature2] == ['ダンスに適しているか', 'エネルギーの強さ']:
    #     plt.ylim(0.5, 1.0)
    #     plt.xlabel("k")
    #     plt.ylabel("score")
    #     plt.plot(list_nn, list_score)
    #     plt.show()

# scoresをDataFrameに変換して表形式で出力
scores_df = pd.DataFrame(scores, columns=['Feature1', 'Feature2', 'Best_k', 'Best_Score'])
scores_df.to_csv('scores.csv', index=False)

# 表形式で出力
print(tabulate(scores_df, headers='keys', tablefmt='pretty'))

# 評価値が最も高かった組み合わせとkの値を取得
best_score_info = max(scores, key=lambda x: x[3])
best_combination = [best_score_info[0], best_score_info[1]]
best_k = best_score_info[2]
best_score = best_score_info[3]
print("総合評価\n組み合わせ：{}\n最高精度：k={}のとき{:.4f}％".format(best_combination, best_k, best_score*100))

# 最適なkで再度機械学習を実行
x = dataset[best_combination]
y = dataset['Label']
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=41)
knn = KNeighborsClassifier(n_neighbors=best_k)  # K=10のK近傍法モデルを使用
knn.fit(x_train, y_train)

# モデルを保存
dump(knn, 'model.joblib')

# 動作確認
# song_features = [0.734, 0.973]  # トウキョウ・シャンディ・ランデヴ
# song_features = [0.463, 0.624]  # ドライフラワー
# song_features_scaled = scaler.transform([song_features])
# prediction = knn.predict(song_features_scaled)
# if prediction[0] == 1:
#     print("この曲はtiktokで\"使われる\"可能性の高い曲です。")
# else:
#     print("この曲はtiktokで\"使われない\"可能性の高い曲です。")
