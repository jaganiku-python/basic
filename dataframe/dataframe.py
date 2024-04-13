"""
https://www.youtube.com/watch?v=ZQZ38rK28Gk
"""

import pandas as pd

#csvデータの読み込み
df = pd.read_csv("weather.csv")

#データの確認
print(df.head(5))
print(df.tail(5))

#特定列の抽出
#列名での処理
df = df[['年月日'
, '平均気温(℃)'
, '最高気温(℃)'
, '最低気温(℃)'
, '降水量の合計(mm)'
, '最深積雪(cm)'
, '平均雲量(10分比)'
, '平均蒸気圧(hPa)'
, '平均風速(m/s)'
, '日照時間(時間)'
]]

#行番号での除外(1列目除外)
df = df[1:]

#データ型の取得
print(df.dtypes)

#サイズ(行数と列数)
print(df.shape)

#index情報
print(df.index)

#要素の取得
#5-10行目,3-6列目
##iloc(番号)
print(df.iloc[4:10, 2:6])

##loc(列名)
print(df.loc[5:10, '最高気温(℃)':'最深積雪(cm)'])

#条件付き要素の取得
df_people = pd.read_csv("people.csv")
#'nationality'が'America'
##条件指定
print(df_people[df_people['nationality'] == 'America'])
##query利用
print(df_people.query('nationality == "America"'))
##isin利用
print(df_people[df_people['nationality'].isin(['America'])])

#'age'が20-29
##条件指定
print(df_people[(df_people['age'] >= 20)&(df_people['age'] < 30)])

##query利用
print(df_people.query('age >= 20 & age < 30'))

#ユニークな値の抽出
print(df_people['nationality'].unique())

#重複列の抽出
##レコードが完全一致
print(df_people.drop_duplicates())
##あるカラムで一致。おそらく上からユニークな値がきたレコードを保持
print(df_people.drop_duplicates(subset = 'nationality'))

#カラム名の変更
##すべてのカラム
df.columns = ['年月日', '平均気温', '最高気温', '最低気温', '降水量の合計', '最深積雪',
       '平均雲量', '平均蒸気圧', '平均風速', '日照時間']
##一部のカラム
df = df.rename(columns={'平均気温' : '平均'})

#データのソート
print(df.sort_values('最高気温', ascending=True))

#カテゴリカルデータをダミー変数化する
print(pd.get_dummies(df_people, columns=['nationality']))

#欠損値の確認、補完、削除
##確認
df.isnull()
##0で補完
df.fillna(0).head(3)
##欠損値を含む行を削除
df.dropna(axis=0).head(3)
##欠損値を含む列を削除
print(df.dropna(axis=1).head(3))

#ユニークな値の確認
df_iris = pd.read_csv('iris.csv')
df_iris['Class'].value_counts()

#各グループの集計値
print(df_iris.groupby('Class').mean())
print(df_iris.groupby('Class').max())
print(df_iris.groupby('Class').min())

#各列の集計値
print(df.max())
print(df.min())
#print(df.mean())
#print(df.median())
print(df_iris.describe())

#csvへエクスポート
df.to_csv('export.csv', index=False)
"""
    match_names = ['team_cd', 'section','date','day_of_week','vs','score', 'away', 'stadium', 'spectator', 'weather', 'agi', 'kagi', 'chance_rate', 'shoot_rate', 'shoot_success_rate', 'dominant_rate', 'at_cbc', 'ps_cbc', 'get_pt', 'def_pt', 'scorer', 'director', 'year', 'created_at']
    to_gcs_match = pd.DataFrame(columns=match_names)

    sd_list=pd.DataFrame(s_list,index=match_names)
    to_gcs_match = pd.concat([to_gcs_match, sd_list.T])
"""