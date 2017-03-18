# coding: utf-8
import json
from api import Restaurant
from datetime import datetime
import time


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


def make_json_pay_load(message, token):
    payload = {
        'response_type': "in_channel",
        'text': str(message),
        'MATTERMOST_TOKEN': token
    }
    json_payload = json.dumps(payload)
    return json_payload




if __name__ == '__main__':
    f = open("./test_result")
    result = json.load(f)
    f.close()
    # response = result['garea_small']


    """
    loop
    get reestraunts information 11:00AM
    """
    CHECK_HOUR = 11
    get_updated_rests = False
    while True:
        now = datetime.now()
        n_hour = now.hour
        n_month = now.month
        n_day = now.day
        # get new restrants in Kosugi at 11 AM
        if n_hour == CHECK_HOUR:
            if not get_updated_rests:
                rests = []
                # get restaurants
                try:
                    response = Restaurant.request_grinavi_restrants()
                    response_json = response.json()
                    rests += Restaurant.parse_response(response=response_json)

                    total_hit_count = int(response_json['total_hit_count'])
                    hit_per_page = 50
                    page_offset = int(response_json['page_offset'])

                    offset_page = 1

                    while total_hit_count - (hit_per_page * page_offset) > 0:
                        # request next page
                        offset_page += 1
                        print "Send Request pages(" + str(offset_page) + ")"
                        response = Restaurant.request_grinavi_restrants(hit_per_page=hit_per_page,
                                                                        offset_page=offset_page)
                        response_json = response.json()
                        rests += Restaurant.parse_response(response=response_json)

                        # update page offset
                        total_hit_count = int(response_json['total_hit_count'])
                        hit_per_page = int(response_json['hit_per_page'])
                        page_offset = int(response_json['page_offset'])

                except:
                    print "Cant't get Restaurants"
                #check updated restaurants in a day
                updated_rets = Restaurant.updated_in_days(rests=rests, day=1, now=now)

                # send to mattermost
                json_payload = Restaurant.send_restaurants(rests=updated_rets)

                # set a flag
                already_get_11am = True
        # reset flag
        if n_hour == 0 and get_updated_rests:
            get_updated_rests = False

        time.sleep(10)


