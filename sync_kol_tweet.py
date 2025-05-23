import csv
import time
import threading
import requests
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
import json
from sqlalchemy.orm import sessionmaker

import models.user
from models.user import KolUsers
def get_7_days_ago_utc():
    # 获取当前 UTC 时间
    utc_now = datetime.now(timezone.utc)
    # 计算 7 天前的时间
    seven_days_ago = utc_now - timedelta(days=7)
    # 格式化成 "YYYY-MM-DD_00:00:00_UTC"
    return seven_days_ago.strftime("%Y-%m-%d_00:00:00_UTC")

def read_kol_db():
    # 创建引擎
    engine = create_engine("postgresql://admin:admin123@18.190.207.151:5432/donkin")
    Session = sessionmaker(bind=engine)
    # 创建会话
    session = Session()

    try:
        # 查询所有用户
        users = session.query(KolUsers).all()
        return users


    finally:
        session.close()

def sync_user_tweets(user_name:str):
    """
    """
    url = f"https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {
        "X-API-Key":"203b820a357d4298a213f127eb090576"
    }


    params={
      "query":json.dumps({"from": '"from:{user_name} since:{date}'.format(date=get_7_days_ago_utc(),user_name = user_name)})
    }
    print(params)
    response = requests.get(url, headers=headers, params=params)
    return response
def save_user_tweets(tweets):
    # 创建引擎
    engine = create_engine("postgresql://admin:admin123@18.190.207.151:5432/donkin")
    Session = sessionmaker(bind=engine)
    kol_tweets=[]
    for tweet in tweets:
        tweet_id = str(tweet['id'])
        print(tweet_id)
        user_id = ''
        if 'author' in tweet and 'id' in tweet['author']:
            user_id = tweet['author']['id']
        text = tweet['text']
        tweet_type = tweet['type']
        url = tweet['url']
        twitter_url = tweet['twitterUrl']
        lang = tweet['lang']
        quoted_tweet_id = None
        if 'quoted_tweet' in tweet and  tweet['quoted_tweet'] is not None and 'id' in tweet['quoted_tweet']:
            quoted_tweet_id = tweet['quoted_tweet']['id']
        tweet_created_at = tweet['createdAt']

        kol_tweet= {
            'tweet_id':tweet_id,
            'user_id':user_id,
            'text':text,
            'type':tweet_type,
            'url':url,
            'twitter_url':twitter_url,
            'lang':lang,
            'quoted_tweet_id':quoted_tweet_id,
            'tweet_created_at':tweet_created_at
        }
        kol_tweets.append(kol_tweet)


    if len(kol_tweets) == 0:
        return
    session = Session()
    # 构建INSERT语句
    stmt = pg_insert(models.user.KolTweets).values(kol_tweets)

    # 设置冲突时更新
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=['tweet_id'],  # 冲突检测的列
        set_={                 # 冲突时要更新的列
            'user_id': stmt.excluded.user_id,
            'text': stmt.excluded.text,
            'type':stmt.excluded.type,
            'url':stmt.excluded.url,
            'twitter_url':stmt.excluded.twitter_url,
            'lang':stmt.excluded.lang,
            'quoted_tweet_id':stmt.excluded.quoted_tweet_id,
            'tweet_created_at':stmt.excluded.tweet_created_at

        }
    )

    # 执行
    session.execute(upsert_stmt)
    session.commit()
    session.close()


    return
def sync_tweet_worker(user_name_list):
    for user_name in user_name_list:

        print(f"正在处理 KOL: user_name={user_name}")

        try:
            #通过x获取kol的近7天推文
            resp = sync_user_tweets(user_name)
            if resp.status_code == 200:
                #存入DB
                save_user_tweets(resp.json()['tweets'])
            else:
                print(f"请求失败，状态码：{resp.status_code}，返回信息：{resp.json()}")
        except Exception as e:
            print(f"请求过程中出现异常：{e}")

def main():
    # 读取 DB的kol users
    kol_data = read_kol_db()
    print(f"读取到 {len(kol_data)} 条 KOL 记录。")

    # 遍历所有 KOL （假设有100个）
    # 创建线程
    threads = []
    user_name_list =[]
    i = 0
    for row in kol_data:
        i+=1
        user_id = row.user_id
        user_name = row.user_name
        print(f"正在处理 KOL: user_id={user_id}，user_name={user_name}")

        user_name_list.append(user_name)
        if i %100 == 0:
            t = threading.Thread(target=sync_tweet_worker, args=(user_name_list,))
            t.start()
            user_name_list = []

    for t in threads:
        t.join()
    if len(user_name_list)!= 0:
        sync_tweet_worker(user_name_list)









if __name__ == '__main__':
    main()
