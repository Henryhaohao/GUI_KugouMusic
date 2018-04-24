# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/2/13--20:40
__author__ = 'Henry'

'''
 爬取酷狗音乐
'''
import requests
import re
import os


# 获取任意歌曲任意页数的一整页歌曲列表:
def list_name(key, page):
    url_search = 'http://www.kugou.com/yy/flask_learning/search.flask_learning#searchType=song&searchKeyWord=%E5%96%9C%E6%AC%A2%E4%BD%A0'  # 就keyword不同
    # 藏着歌曲信息的js请求地址:
    # 注意: 一页最多30首歌(pagesize=30),当前页面(page=1),当访问到json()文件中"error_code" : 149时:即表示后面已经没有歌了;正常的页面"error_code" : 0
    # 后面不要还不行,容易出错:'&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0'
    # url_js = 'http://songsearch.kugou.com/song_search_v2?keyword=%E5%96%9C%E6%AC%A2%E4%BD%A0&page=1&pagesize=30'
    url_js = 'http://songsearch.kugou.com/song_search_v2?keyword=%s&page=%s&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1519293500820' % (
    key, page)
    html = requests.get(url_js).json()
    # print(html)

    # 取出第一页第一首歌歌曲的歌手名-歌名(一起的),hash和album_id:
    info = html['data']['lists']
    # print(info)
    name_list = []
    for i in range(len(html['data']['lists'])):
        song_name = html['data']['lists'][i]['FileName']
        song_name = re.sub('<em>', '', song_name)
        song_name = re.sub('</em>', '', song_name)
        name_list.append(song_name)
        # print('song_name:'+song_name)   #去掉中间的<em>和</em>
    return name_list


# 测试函数:
# list_name('喜欢你','1')


# 获取任意歌曲任意一页的任意一首的歌名:
def song_name(key, page, i):
    url_search = 'http://www.kugou.com/yy/flask_learning/search.flask_learning#searchType=song&searchKeyWord=%E5%96%9C%E6%AC%A2%E4%BD%A0'  # 就keyword不同
    # 藏着歌曲信息的js请求地址:
    # 注意: 一页最多30首歌(pagesize=30),当前页面(page=1),当访问到json()文件中"error_code" : 149时:即表示后面已经没有歌了;正常的页面"error_code" : 0
    # 后面不要还不行,容易出错:'&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0'
    # url_js = 'http://songsearch.kugou.com/song_search_v2?keyword=%E5%96%9C%E6%AC%A2%E4%BD%A0&page=1&pagesize=30'
    url_js = 'http://songsearch.kugou.com/song_search_v2?keyword=%s&page=%s&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1519293500820' % (
        key, page)
    html = requests.get(url_js).json()
    # print(html)

    # 取出第一页第一首歌歌曲的歌手名-歌名(一起的),hash和album_id:
    info = html['data']['lists']
    # print(info)
    song_name = html['data']['lists'][i - 1]['FileName']
    song_name = re.sub('<em>', '', song_name)
    song_name = re.sub('</em>', '', song_name)
    # print('song_name:'+song_name)   #去掉中间的<em>和</em>
    return song_name


# 测试函数
song_name('喜欢你', '1', 1)


# 获取任意歌曲任意页数任意第几首歌的下载地址:
def list_url(key, page, i):
    url_js = 'http://songsearch.kugou.com/song_search_v2?keyword=%s&page=%s&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1519293500820' % (
    key, page)
    html = requests.get(url_js).json()
    # print(html)

    # 取出第一页第一首歌歌曲的歌手名-歌名(一起的),hash和album_id:
    info = html['data']['lists']
    # print(info)
    hash = html['data']['lists'][i - 1]['FileHash']
    # print('hash:'+hash)
    album_id = html['data']['lists'][i - 1]['AlbumID']
    # print('album_id:'+album_id)
    song_name = html['data']['lists'][i - 1]['FileName']
    # song_name = song_name[:-5]
    song_name = re.sub('<em>', '', song_name)
    song_name = re.sub('</em>', '', song_name)
    # print('song_name:'+song_name)   #去掉中间的<em>和</em>

    # 拼接出请求得到下载地址的网址:(例:'http://www.kugou.com/yy/index.php?r=play/getdata&hash=41C2E4AB5660EAE04021C5893E055F50&album_id=557512')
    url_info = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s&album_id=%s' % (hash, album_id)
    # print('download_url:'+url_info)

    # 请求得到歌曲下载地址的网址:
    html_info = requests.get(url_info).json()
    # print(html_info)

    # 取出歌曲的歌名/下载地址/歌词...:
    play_url = html_info['data']['play_url']
    # print('play_url:'+play_url)

    # 下载歌曲(还自带了歌词):
    if os.path.exists('E:\\Python_Project\\study_python\\kugou_music\\' + song_name + '.mp3'):
        # print('存在此歌曲')
        pass
    else:
        mp3 = requests.get(play_url).content
        open('E:\\Python_Project\\study_python\\kugou_music\\' + song_name + '.mp3', 'wb').write(mp3)

# 测试函数:
# list_url('喜欢你','1',1)
