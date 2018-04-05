import bs4
import os
import os.path, time, re
import urllib
import json
import random
import imghdr
import subprocess
import ssl
import argparse
from PIL import Image
from os import makedirs
from bs4 import BeautifulSoup as Soup
from datetime import datetime

PROXIES = {
    'http' : 'xxx.local:8080',
    'https' : 'xxx.local:8080',
    'ftp' : 'xxx.local:8080'
}

def set_unverifited_ssl():
    """
    信用できないSSL証明書を信用する（望ましい方法ではない。）
    """
    ssl._create_default_https_context = ssl._create_unverified_context

def install_custom_opener():
    """
    プロキシに対する対策として、カスタムのopenrをインストールする
    """
    proxy_handler = urllib.request.ProxyHandler(PROXIES)
    opener = urllib.request.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')]
    urllib.request.install_opener(opener)

def resize_image(input_path, output_path):
    # 画像フォルダの中のファイル名取得
    list_input_path = os.listdir(input_path)

    for number in range(0, len(list_input_path)):
        # 画像ファイルを開く
        img = Image.open(input_path + "/" + list_input_path[number], 'r')

        # img.resize((480, 300), Image.LANCZOS)は、リサイズするサイズの設定、フィルタの設定
        img_resize_lanczos = img.resize((480, 300), Image.LANCZOS)
        img_resize_lanczos = img_resize_lanczos.convert("RGB")
        # リサイズした画像の保存
        img_resize_lanczos.save(output_path + "/" + list_input_path[number], quality = 100)

def get_img_links(url):
    print('url=', url)

    request = urllib.request.urlopen(url)
    html = request.read()

    # 文字コードのリストを作成
    encoding_list = ["cp932", "utf-8", "utf_8", "euc_jp",
                    "euc_jis_2004", "euc_jisx0213", "shift_jis",
                    "shift_jis_2004", "shift_jisx0213", "iso2022jp",
                    "iso2022_jp_1", "iso2022_jp_2", "iso2022_jp_3",
                    "iso2022_jp_ext", "latin_1", "ascii"]

    for enc in encoding_list:
        try:
            html.decode(enc)
            break
        except:
            enc = None

    resources = []

    # BeautifulSoupオブジェクトを作成
    soup = bs4.BeautifulSoup(html,'lxml')

    # htmlのすべてのimgタグの中のsrc属性の内容を取得
    for img_tag in soup.find_all("img"):
        src_str = img_tag.get("src")
        resources.append(src_str)

    # srcの内容を表示
    array_img = []
    for resource in resources:
        if resource.startswith('http') == True:
            if resource.endswith('.gif') == False:
                array_img.append(resource)

    return array_img


def save_image(imageurl, num, keyword, basefolderpath):
    print('imageurl=', imageurl)

    imagefolderpath = basefolderpath + keyword
    if os.path.isdir(imagefolderpath) == False:
        makedirs(imagefolderpath)

    tempfilepath = imagefolderpath + '/tmp'
    if os.path.isfile(tempfilepath) == True:
        os.remove(tempfilepath)

    urllib.request.urlretrieve(imageurl, tempfilepath)
    sleepnum = random.uniform(1, 1.4)
    time.sleep(sleepnum) # 礼儀として一定時間スリープ

    imagetype = imghdr.what(tempfilepath)
    if not(type(imagetype) is None):
        filename =  imagefolderpath + '/' + keyword + '_{0:0>5}'.format(num) + '.' + imagetype
        os.rename(tempfilepath, filename)

def search_images_fromstartnum(keyword, startnum, basefolderpath):
    print('startnum=', startnum)

    qkeyword = urllib.parse.quote(keyword)

    code = '&ei=UTF-8'
    phrase = '?p=' + qkeyword
    start = '&b=' + str(startnum)

    # https://search.yahoo.co.jp/image/search?p=%E7%8C%AB&ei=UTF-8&b=1
    # https://search.yahoo.co.jp/image/search?p=%E7%8C%AB&ei=UTF-8&b=26

    url = 'https://search.yahoo.co.jp/image/search' + phrase + code + start

    array_img = get_img_links(url)

    for x in range(0, len(array_img)):
        imageurl = array_img[x]
        imagenum = startnum + x
        save_image(imageurl, imagenum, keyword, basefolderpath)

def search_images(keywords,searchcount):
    now = datetime.now()
    basefolderpath = '../image/{0:%Y%m%d-%H%M%S}/'.format(now)

    print('keywords=', keywords)
    print('basefolderpath=', basefolderpath)

    for x in range(len(keywords)):
        keyword = keywords[x]
        print('keyword=', keyword)
        print('searchcount=', searchcount)
        for num in range(1, searchcount + 2, 25):
            search_images_fromstartnum(keywords[x], num, basefolderpath)    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("searchcount", type=int)
    parser.add_argument("keywords")
    args = parser.parse_args()

    # set_unverifited_ssl()
    install_custom_opener()

    keywords = args.keywords.split(',')
    # keywords = ["猫","犬"]
    # keywords = ["cars","numbers","scenery","people","dogs","cats","animals"]
    searchcount = args.searchcount

    search_images(keywords, searchcount)
