# coding: utf-8
import requests
import json
import sys
from datetime import datetime as dt
import datetime
from user import USER_KEY
from mattermost import make_json_pay_load, send_message

SITE_URL='http://api.gnavi.co.jp/RestSearchAPI/20150630/'


def request_grinavi_restrants(hit_per_page=50, offset_page=1):
    param = {
        'keyid': USER_KEY,
        'format': 'json',
        'areacode_s': 'AREAS2310',  # AREAS2310:武蔵小杉・元住吉
        'offset_page': offset_page,
        'hit_per_page': hit_per_page
    }
    response = None
    try:
        response = requests.get(SITE_URL, params=param)
    except:
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


def updated_in_days(rests=None, day=1, now=None):
    updated_rests = []
    for r in rests:
        if now - r.update_date < datetime.timedelta(days=day):
            updated_rests.append(r)

    return updated_rests

def send_restaurants(rests=None):

    header = '|店名|住所|¥n|---|---|¥n'
    body = ''

    if len(rests) > 0:
        for r in rests:
            body += '|[' + r.name + '](' + r.url + ')|' + r.address + '|¥n'
        # send table to mattermost
        json_payload = make_json_pay_load(message=header+body)
        send_message(json=json_payload)

    return None

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
        self.opentime = data['opentime'].encode('utf-8')
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
