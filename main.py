# coding: utf-8
import requests
import json
from api import Restaurant
from user import USER_KEY

"""
AREAL2322:横浜・東神奈川  PREF14:神奈川県
AREAL2336:みなとみらい・関内・中華街  PREF14:神奈川県
AREAL2302:川崎・鶴見  PREF14:神奈川県
AREAL2310:武蔵小杉・日吉・綱島  PREF14:神奈川県
AREAL2354:新横浜・センター南・鴨居  PREF14:神奈川県
AREAL2360:上大岡・金沢文庫・新杉田  PREF14:神奈川県
AREAL2372:横須賀・久里浜・三浦半島  PREF14:神奈川県
AREAL2352:戸塚・東戸塚  PREF14:神奈川県
AREAL2374:鎌倉・大船・逗子  PREF14:神奈川県
AREAL2375:藤沢・茅ヶ崎・平塚  PREF14:神奈川県
AREAL2308:溝の口・たまプラーザ・青葉台  PREF14:神奈川県
AREAL2294:登戸・向ヶ丘遊園・新百合ヶ丘  PREF14:神奈川県
"""

"""
AREAS2336:横浜中華街
AREAS2340:横浜元町
AREAS2342:山下公園
AREAS2344:本牧・山手
AREAS2302:川崎
AREAS2348:鶴見
AREAS2310:武蔵小杉・元住吉
AREAS2356:日吉・綱島
AREAS2398:白楽・反町
AREAS2354:新横浜
"""

if __name__ == '__main__':
    response = Restaurant.request_grinavi_restrants()
    rests = Restaurant.parse_response(response=response)
    for i in rests:
        info = i.get_short_info()
        print '%s(%s): %s¥n%s¥n%s' % (info['name'], info['url'], info['pr_short'], info['address'], info['tel'])



