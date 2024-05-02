"""
下記のようなページのデータ取得(リストにある全チーム分)
https://www.football-lab.jp/oita/match/?year=2023

事前準備：
・GCPのCLI設定 https://cloud.google.com/docs/authentication/external/set-up-adc
・環境変数の設定
PROJCET:対象データを格納したいプロジェクト
BUCKET:対象データを格納したいバケット
FOLDER:対象データを格納したいフォルダ
・各moduleのインポート

メモ：
基本的な動作は、他のページになったとしても同様
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime, timedelta, timezone, date
from google.cloud import storage
import os

logger = logging.getLogger(__name__)
PROJECT = os.environ['PROJECT']
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
MATCH_NAMES = ['team_cd', 'section', 'date', 'day_of_week', 'vs', 'score', 'away', 'stadium', 'spectator', 'weather', 'agi', 'kagi', 'chance_rate', 'shoot_rate', 'shoot_success_rate', 'dominant_rate', 'at_cbc', 'ps_cbc', 'get_pt', 'def_pt', 'scorer', 'director', 'year', 'created_at']



#bsオブジェクトの作成
def make_bs_data(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, 'html.parser')
    return bs

#bsオブジェクトに対して、特定タグの情報取得
def get_bs_tag(bs_data, tag):
    bs_tag = bs_data.find_all(tag)
    return bs_tag

#bsオブジェクトに対して、特定クラスの情報取得
def get_bs_class(bs_data, cls):
    bs_class = bs_data.find_all(class_=cls)
    return bs_class  

#dataframeの結合用の関数
def merge_dataframe(dataa, datab):
    to_gcs_action = pd.concat([dataa, datab])
    to_gcs_action = to_gcs_action.reset_index(drop=True)
    return to_gcs_action

#あるチーム単位での、gcsにアップロードする用のデータ作成
def match_to_gcp(team, bs_data, year, time):
    #必要な情報のカラム
    #最終返り値用の変数
    to_gcs_match = pd.DataFrame(columns=MATCH_NAMES)
    #あるタグ内の2番目の要素から取得（実データ参照）
    for i in range(2,len(bs_data)):
        #各マッチデータ格納用の変数
        s_list=[team]
        for bs_ui in bs_data[i].find_all('td'):          
            bs_text = bs_ui.text
            s_list.append(bs_text)
        s_list.append(year)        
        s_list.append(time)

        try:
            sd_list=pd.DataFrame(s_list, index=MATCH_NAMES)
            to_gcs_match = pd.concat([to_gcs_match, sd_list.T])
        except Exception as e:
            logger.info("gcsへのアップロードに失敗しました")
            pass

    to_gcs_match=to_gcs_match.reset_index(drop=True)
    return to_gcs_match

#全てのチームに対して、gcsにアップロードする用のデータ作成
def get_all_match(team_list, year_list, created_at):  
    for _ in range(3):  # 最大3回実行
        try:
            #import用ファイル作成
            to_gcs_match_all = pd.DataFrame(columns=MATCH_NAMES)
        
            for t in team_list:
                for y in year_list:
                    #アクセス用URL作成
                    url = 'https://www.football-lab.jp/' + t + '/match/?year=' + y

                    #データ取得用bsオブジェクト作成
                    bs_data = make_bs_data(url)    
                    bs_data_tr = get_bs_tag(bs_data, 'tr') 

                    #あるチーム単位のデータ取得
                    tmp_match = match_to_gcp(t, bs_data_tr, y, created_at)
                    to_gcs_match_all = merge_dataframe(to_gcs_match_all, tmp_match)
        except Exception as e:
            logger.info("チーム単位でのデータ取得に失敗しました。")
            pass
        else:
            break
    else:
        pass
    return to_gcs_match_all

#gcsにアップロード
def to_gcs(to_data, bucket, folder, file, today):
    data = to_data
    bucket_name = bucket
    folder_name = folder

    #西暦の20xx年のxxの部分のみであるため、変換対応
    if today.year < 10:
        year = '0' + str(today.year)
    else:
        year = str(today.year)
    #10未満の月は、0が必要
    if today.month < 10:
        month = '0' + str(today.month)
    else:
        month = str(today.month)
    
    #10未満の日は、0が必要
    if today.day < 10:
        day = '0' + str(today.day)
    else:
        day = str(today.day)

    created_at = year+month+day
    file_name = f"{created_at}/{file}.csv"

    # GCSクライアント初期化
    client = storage.Client(project=PROJECT)

    # バケットオブジェクト取得
    bucket = client.get_bucket(bucket_name)

    # 保存先フォルダとファイル名作成
    blob = bucket.blob(os.path.join(folder_name, file_name))   

    # データをGCSへアップロードする
    res = blob.upload_from_string(
        data=data.to_csv(sep=",", index=False),
        content_type="text/csv")

    print(f"File {file_name} uploaded to {folder_name}.")
    print(res)

    
    
def main(event=None, callback=None):
    #全チームid
    team_list = [     
      'sapp',
      'send',
      'kasm',
      'uraw',
      'fctk',
      'ka-f',
      'y-fm',
      'shon',
      'mats',
      'shim',
      'iwat',
      'nago',
      'g-os',
      'c-os',
      'kobe',
      'hiro',
      'tosu',
      'oita',
      'yama',
      'mito',
      'toch',
      'omiy',
      'chib',
      'kasw',
      'tk-v',
      'mcd',
      'y-fc',
      'kofu',
      'niig',
      'kana']

    #実行日取得
    JST = timezone(timedelta(hours=+9), 'JST')
    today = datetime.now(JST)
    #日付の桁数対応
    if today.year < 10:
        year = '0' + str(today.year)
    else:
        year = str(today.year)

    if today.month < 10:
        month = '0' + str(today.month)
    else:
        month = str(today.month)

    if today.day < 10:
        day = '0' + str(today.day)
    else:
        day = str(today.day)

    created_at = year+month+day
    #２年分を実行する
    year_list = [str(today.year), str(today.year - 1)]
    
    logger.info('execute get_all_match')  
    match_data = get_all_match(team_list, year_list, created_at)  
    logger.info('finished get_all_match')  
    
    #文字列→日付の対応
    match_data.iloc[:,2] = match_data.iloc[:,22] + '.' + match_data.iloc[:,2]

    logger.info('execute to_gcs match')      
    to_gcs(match_data, BUCKET, FOLDER, "match_1", today)
    logger.info('finished to_gcs match')  
        
    return(1)

#ローカルデバッグ用
#main()