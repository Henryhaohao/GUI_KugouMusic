# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/2/22--18:39
__author__ = 'Henry'

'''
酷狗音乐桌面版(引用爬虫:API_music_kugou.py)
'''

from tkinter import *
import tkinter.messagebox
import pygame  # 方法三:播放MP3/wav音频 (此方法好用!!!)
import API_music_kugou

# 添加全局变量,用于翻页
keyword = 0
page = 1
name = ''


# 播放
def play(e):  # 注意:这里必须传递一个e参数,不然报错!!!
    # 先下载下来:
    global keyword
    global page
    global content  # 因为list根据页数也跟着不同,所以要定义成全局变量
    global name
    content = list.get(list.curselection())
    num = content.split('.')[0]
    # name= content.split('.')[1]  #因为有的个名字中含有'.',所以不能用这种方法获取歌名(例如:G.E.M.邓紫棋.MP3)
    num = int(num)
    name = API_music_kugou.song_name(keyword, page, num)
    # print(type(num))
    # keyword = text_1.get()
    API_music_kugou.list_url(keyword, page, num)
    # 再开始播放:
    file = 'E:\\Python_Project\\study_python\\kugou_music\\' + name + '.mp3'
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    list.delete(list.size() - 1, END)  # 保留前面的不变;索引值
    list.insert(END, '当前正在播放的歌曲:' + name)


# 暂停播放
def pause():
    pygame.mixer.music.pause()


# 继续播放
def unpause():
    pygame.mixer.music.unpause()


# 搜索音乐并插入音乐列表
def search_list():
    global keyword
    global name
    keyword = text_1.get()  # 获取搜索内容
    name_list = API_music_kugou.list_name(keyword, page)  # 引入爬虫的搜索函数
    list.delete(0, END)
    for i in range(len(name_list)):
        list.insert(END, str(i + 1) + '.' + name_list[i])
    # 当前第一页
    list.insert(END, '当前为第' + str(page) + '页')
    # 当前正在播放的歌曲
    try:
        list.insert(END, '当前正在播放的歌曲:' + name)
    except:
        list.insert(END, '当前正在播放的歌曲:没有正在播放的歌曲~')


# 下一页
def next():
    global page
    global keyword
    global name
    try:
        page += 1
        name_list = API_music_kugou.list_name(keyword, page)
        list.delete(0, END)
        for i in range(len(name_list)):
            list.insert(END, str(i + 1) + '.' + name_list[i])
        # 当前为第page页
        list.insert(END, '当前为第' + str(page) + '页')
    except:
        tkinter.messagebox._show('温馨提示', '抱歉,没有下一页喽亲~')
    list.insert(END, '当前正在播放的歌曲:' + name)


# 上一页
def last():
    global page
    global keyword
    global name
    try:
        if page >= 2:
            page -= 1
            name_list = API_music_kugou.list_name(keyword, page)
            list.delete(0, END)
            for i in range(len(name_list)):
                list.insert(END, str(i + 1) + '.' + name_list[i])
            # 当前为第page页
            list.insert(END, '当前为第' + str(page) + '页')
    except:
        tkinter.messagebox._show('温馨提示', '抱歉,没有上一页喽亲~')
    list.insert(END, '当前正在播放的歌曲:' + name)


# 界面部分:
root = Tk()
root.title('酷狗音乐')
root.geometry('+780+300')

# 搜索框:
Label(root, text='歌名或歌手名', font=('黑体', 20, 'bold'), bg='blue').grid(row=0, column=0, sticky=N + S + E + W)

text_1 = Entry(root, font=('黑体', 20, 'bold'))
text_1.grid(row=0, column=1)

search = Button(root, text='搜索', font=('黑体', 20, 'bold'), bg='red', command=search_list).grid(row=0, column=2,
                                                                                              sticky=N + S + E + W)

Label(root, text='双击歌名即可播放', font=('黑体', 16, 'bold')).grid(row=0, column=3, sticky=N + S)

# 歌曲列表(双击歌曲播放):
list = Listbox(root, width=80, height=30, font=('黑体', 15, 'bold'),
               bg='#9AFF9A')  # 创建个列表框,用来打印出音乐列表;要写个宽度,不然显示不全,占不了5个单元格
list.bind('<Double-Button-1>', play)  # 可以双击列表,返回play函数
list.grid(row=1, columnspan=5, sticky=N + S + E + W)  # span相当于合并单元格,因为row=0上面一行有5个单元格
# sticky=N+S+E+W:上下左右全部对齐

# 暂停播放按钮:
Button(root, text='暂停播放', font=('黑体', 20, 'bold'), bg='#96CDCD', command=pause).grid(row=2, column=0)

# 继续播放按钮:
Button(root, text='继续播放', font=('黑体', 20, 'bold'), bg='#96CDCD', command=unpause).grid(row=2, column=1)

# 上一页按钮:
Button(root, text='上一页', font=('黑体', 20, 'bold'), bg='#FFEC8B', command=last).grid(row=2, column=2)

# 下一页按钮:
Button(root, text='下一页', font=('黑体', 20, 'bold'), bg='#FFEC8B', command=next).grid(row=2, column=3)

# 退出按钮:
Button(root, text='退出', font=('黑体', 20, 'bold'), bg='grey', command=root.quit).grid(row=2, column=4)

root.mainloop()
