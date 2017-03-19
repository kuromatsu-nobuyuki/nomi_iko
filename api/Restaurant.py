# coding: utf-8
import requests
import json
import sys
import os
import shutil
from datetime import datetime as dt
import datetime
from user import USER_KEY
from mattermost import make_json_pay_load, send_message

SITE_URL='http://api.gnavi.co.jp/RestSearchAPI/20150630/'
known_restaurants = []
CSV_PATH = '/root/data/rests.csv'


def request_grinavi_restrants(hit_per_page=50, offset_page=1, areacode_s='AREAS2310'):
    param = {
        'keyid': USER_KEY,
        'format': 'json',
        'areacode_s': areacode_s,  # AREAS2310:武蔵小杉・元住吉
        'offset_page': offset_page,
        'hit_per_page': hit_per_page
    }
    response = None
    try:
        response = requests.get(SITE_URL, params=param)
    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
        print("message:{0}".format(e.message))
        print("{0}".format(e))
        print "fail to get Restaurants."
    return response

def parse_response(response=None):
    """

    :param data: json format response returned by griunavi web api
    :return: Restaurants list
    """
    restaurants = response['rest']
    rest_list = []
    for i in restaurants:
        r = Restaurant(data=i)
        rest_list.append(r)
    return rest_list


def request_all_restrants(area_s=None):
    """
    get all restaurants in area_S
    :param area_s: area_name
    :return: list of Restaurant Class
    """
    HIT_PER_PAGE = 50
    rests = []
    # get restaurants
    try:
        response = request_grinavi_restrants()
        response_json = response.json()
        rests += parse_response(response=response_json)

        total_hit_count = int(response_json['total_hit_count'])
        hit_per_page = HIT_PER_PAGE
        page_offset = int(response_json['page_offset'])

        while total_hit_count - (hit_per_page * page_offset) > 0:
            # request next page
            page_offset += 1
            print "Send Request pages(" + str(page_offset) + ")"
            response = request_grinavi_restrants(hit_per_page=hit_per_page,
                                                            offset_page=page_offset)
            response_json = response.json()
            rests += parse_response(response=response_json)

            # update page offset
            total_hit_count = int(response_json['total_hit_count'])
            hit_per_page = int(response_json['hit_per_page'])
            page_offset = int(response_json['page_offset'])

    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
        print("message:{0}".format(e.message))
        print("{0}".format(e))
        print "Cant't get Restaurants"
    return


def updated_in_days(rests=None, day=1, now=None):
    updated_rests = []
    for r in rests:
        if now - r.update_date < datetime.timedelta(days=day):
            updated_rests.append(r)

    return updated_rests

def send_restaurants(rests=None):

    header = '|店名|住所|\n|---|---|\n'
    body = ''

    if len(rests) > 0:
        for r in rests:
            record = '|[' + r.name + '](' + r.url + ')|' + r.address + '|\n'
            if len(header) + len(body) + len(record) > 4000:
                # mattermost can't get over 4000 character
                json_payload = make_json_pay_load(message=header + body)
                send_message(json=json_payload)
                body = ''
            body += record
        # send table to mattermost
        json_payload = make_json_pay_load(message=header+body)
        send_message(json=json_payload)

    return None


def get_unknown_restaurants(rests=None):
    """
    return unknwon restaurants list.
    :param rests: list of Restaurant classe
    :return: list of Restaurant class
    """
    unknown_restaurants = []
    for rest in rests:
        if not rest.id in known_restaurants:
            unknown_restaurants.append(rest)
    return unknown_restaurants

def update_knwon_restaurants(unknwon_rests=None):
    """
    update knwon restaurant list and save to file.
    :param unknwon_rests:
    :return:
    """
    if len(unknwon_rests) > 0:
        known_restaurants.append(unknwon_rests)
    write_known_restaurants()
    return


def write_known_restaurants():
    try:
        # write Restaurant as tmp file
        tmp_filepath = CSV_PATH + '.tmp'
        f = open(tmp_filepath, 'w')
        for rest_id in known_restaurants:
            f.write(str(rest_id) + '¥n')
        f.close()
        # copy tmpfile to Restaurants file
        shutil.copy2(tmp_filepath, CSV_PATH)
    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
        print("message:{0}".format(e.message))
        print("{0}".format(e))
        print "Failed to save Restaurants to %s" % CSV_PATH
    return


def read_known_restaurants():
    """
    read Restaurant file fron local disk.
    :return: True: read file, False: there is no file.
    """
    if not os.path.exists(CSV_PATH):
        print "There is no Restaurant in %s" % CSV_PATH
        return False
    try:
        f = open(CSV_PATH, 'r')
        lines = f.readlines()
        f.close()

        # delete old known Restaurants
        known_restaurants = []

        # update Restaurants list
        for line in lines:
            known_restaurants.append(str.strip(line))

    except Exception as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
        print("message:{0}".format(e.message))
        print("{0}".format(e))
        print "Failed to read Restaurants in %s" % CSV_PATH
        sys.exit(1)

    return True



def is_str(data=None):
    """
    check data's type is str
    :param data:
    :return:
    """
    if isinstance(data, str) or isinstance(data, unicode):
        return True
    else:
        return False


class Restaurant():
    id = ''
    update_date = None
    name = u'名無しのお店'
    name_kana = u'ナナシノオミセ'
    latitude = 0
    longitude = 0
    category = 'None Category'
    url = ''
    url_mobile = ''
    coupon_url = {
        'pc': '',
        'mobile': ''
    }
    image_url = {
        'shop_image1': '',
        'shop_image2': '',
        'qrcode': ''
    }
    address = ''
    tel = ''
    tel_sub = ''
    fax = ''
    opentime = ''
    holiday = ''
    access = {
        'line': '',
        'station': '',
        'station_exit': '',
        'walk': 0,
        'note': ''
    }
    parking_lots = 0,
    pr = {
        'pr_short': '',
        'pr_long': ''
    }
    #code = {
    #    'areacode':,
    #    'areaname':,
    #    'prefcode':,
    #    'prefname':,
    #    'areacode_s':,
    #    'areaname_s':,
    #    'category_code_l': {
    #
    #                       },
    #}
    budget = 0
    party = 0
    lunch = 0
    credit_card = ''
    e_money = ''
    flags = {
        'mobile_site': 0,
        'mobile_coupon': 0,
        'pc_coupon': 0
    }

    def __init__(self, data=None):
        if json is None:
            print "Restaurant's record is None."
            sys.exit(1)

        self.id = data['id'].encode('utf-8')
        self.update_date = dt.strptime(data['update_date'], '%Y-%m-%d %H:%M:%S')
        self.name = data['name'].encode('utf-8')
        if len(data['name_kana']) != 0:
            self.name_kana = data['name_kana'].encode('utf-8')
        # latitude
        # longitude
        # category
        if len(data['url']) != 0:
            self.url = data['url'].encode('utf-8')
        if len(data['url_mobile']) != 0:
            self.url_mobile = data['url_mobile'].encode('utf-8')
        coupon_url = data['coupon_url']
        if len(coupon_url['pc']) != 0:
            self.coupon_url['pc'] = coupon_url['pc'].encode('utf-8')
        if len(coupon_url['mobile']) != 0:
            self.coupon_url['mobile'] = coupon_url['mobile'].encode('utf-8')
        image_url = data['image_url']
        if len(image_url['shop_image1']) != 0:
            self.image_url['shop_image1'] = image_url['shop_image1'].encode('utf-8')
        if len(image_url['shop_image2']) != 0:
            self.image_url['shop_image2'] = image_url['shop_image2'].encode('utf-8')
        if len(image_url['qrcode']) != 0:
            self.image_url['qrcode'] = image_url['qrcode'].encode('utf-8')
        if len(data['address']) != 0:
            self.address = data['address'].encode('utf-8')
        if len(data['tel']) != 0:
            self.tel = data['tel'].encode('utf-8')
        # tel_sub
        # fax
        if 'opentime' in data and is_str(data['opentime']):
            self.opentime = data['opentime'].encode('utf-8')
        if 'holiday' in data and is_str(data['holiday']):
            self.holiday = data['holiday'].encode('utf-8')
        access = data['access']
        if len(access['line']) != 0:
            self.access['line'] = access['line'].encode('utf-8')
        if len(access['station']) != 0:
            self.access['station'] = access['station'].encode('utf-8')
        if len(access['station_exit']) != 0:
            self.access['station_exit'] = access['station_exit'].encode('utf-8')
        if len(access['walk']) != 0:
            self.access['walk'] = access['walk'].encode('utf-8')
        if len(access['note']) != 0:
            self.access['note'] = access['note'].encode('utf-8')
        if len(data['parking_lots']) != 0:
            self.parking_lots = data['parking_lots'].encode('utf-8')
        pr = data['pr']
        if len(pr['pr_short']) != 0:
            self.pr['pr_short'] = pr['pr_short'].encode('utf-8')
        if len(pr['pr_long']) != 0:
            self.pr['pr_long'] = pr['pr_long'].encode('utf-8')
        # code
        if len(data['budget']) != 0:
            self.budget = data['budget'].encode('utf-8')
        if len(data['party']) != 0:
            self.party = data['party'].encode('utf-8')
        if len(data['credit_card']) != 0:
            self.credit_card = data['credit_card'].encode('utf-8')
        if len(data['e_money']) != 0:
            self.e_money = data['e_money'].encode('utf-8')
        flags = data['flags']
        if len(flags['mobile_site']) != 0:
            self.flags['mobile_site'] = flags['mobile_site'].encode('utf-8')
        if len(flags['mobile_coupon']) != 0:
            self.flags['mobile_coupon'] = flags['mobile_coupon'].encode('utf-8')
        if len(flags['pc_coupon']) != 0:
            self.flags['pc_coupon'] = flags['pc_coupon'].encode('utf-8')

    def get_short_info(self):
        restaurant_info = {
            'name': self.name,
            'url': self.url,
            'address': self.address,
            'tel': self.tel,
            'pr_short': self.pr['pr_short']
        }
        return restaurant_info
