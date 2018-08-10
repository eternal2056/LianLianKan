#coding=utf-8
#连连看外挂

import win32gui
import win32api
import win32con
from PIL import ImageGrab
import time
from numpy import *
from ctypes import *
import random

#比较两个是否一样的算法
def channel_compare(cha_a,cha_b):
    sum_a = sum([i * v for i, v in enumerate(cha_a)])
    sum_b = sum([i * v for i, v in enumerate(cha_b)])
    if sum_a + sum_b > 0:
        diff_channel = abs(sum_a - sum_b) * 10000 / max(sum_a, sum_b)
    else:
        diff_channel = abs(sum_a - sum_b) * 10000 / max(sum_a, sum_b)
    return diff_channel
def image_compare(image_a,image_b):
    histogram_a = image_a.histogram()
    histogram_b = image_b.histogram()
    if len(histogram_a) != 768 or len(histogram_b) != 768:
        print("error!!!")
        return None
    diff_red = channel_compare(histogram_a[:256], histogram_b[:256])
    diff_green = channel_compare(histogram_a[256:512], histogram_b[256:512])
    diff_blue = channel_compare(histogram_a[512:768],histogram_b[512:768])
    return diff_red, diff_green, diff_blue
#一条线上有没有障碍的判断
def zhilian_panduan(suanfa_1, suanfa_2, suanfa_3, suanfa_4):
    nenglian = False
    if suanfa_1 < suanfa_3:
        if suanfa_1 + 1 == suanfa_3:
            nenglian = True
        else:
            for zhilian_1 in range(suanfa_1 + 1, suanfa_3):
                if result[zhilian_1][suanfa_2] == max_xx:
                    nenglian = True
                else:
                    nenglian = False
                    break
    if suanfa_1 > suanfa_3:
        if suanfa_1 - 1 == suanfa_3:
            nenglian = True
        else:
            for zhilian_2 in range(suanfa_3 + 1, suanfa_1):
                if result[zhilian_2][suanfa_2] == max_xx:
                    nenglian = True
                else:
                    nenglian = False
                    break
    if suanfa_2 < suanfa_4:
        if suanfa_2 + 1 == suanfa_4:
            nenglian = True
        else:
            for zhilian_3 in range(suanfa_2 + 1, suanfa_4):
                if result[suanfa_1][zhilian_3] == max_xx:
                    nenglian = True
                else:
                    nenglian = False
                    break
    if suanfa_2 > suanfa_4:
        if suanfa_2 - 1 == suanfa_4:
            nenglian = True
        else:
            for zhilian_4 in range(suanfa_4 + 1, suanfa_2):
                if result[suanfa_1][zhilian_4] == max_xx:
                    nenglian = True
                else:
                    nenglian = False
                    break
    return nenglian
#两条线上有没有障碍的判断
def yizhe_panduan(suanfa_1,suanfa_2,suanfa_3,suanfa_4):
    if result[suanfa_3][suanfa_2] == max_xx:
        if zhilian_panduan(suanfa_3,suanfa_2,suanfa_3,suanfa_4):
            if zhilian_panduan(suanfa_3,suanfa_2,suanfa_1,suanfa_2):
                return True
    if result[suanfa_1][suanfa_4] == max_xx:
        if zhilian_panduan(suanfa_1,suanfa_4,suanfa_3,suanfa_4):
            if zhilian_panduan(suanfa_1,suanfa_4,suanfa_1,suanfa_2):
                return True
    return False
#三条线上有没有障碍的判断
#某坐标的广度判断
def guangdu_panduan(suanfa_1,suanfa_2):
    y = suanfa_1
    x = suanfa_2
    guangdu = []
    for x in range(suanfa_1 + 1,11):
        if result[x][suanfa_2] == max_xx:
            guangdu.append([x,suanfa_2])
        else:
            break
    for x in range(suanfa_1, -1,-1):
        if result[x][suanfa_2] == max_xx:
            guangdu.append([x,suanfa_2])
        else:
            break
    for y in range(suanfa_2 + 1,19):
        if result[suanfa_1][y] == max_xx:
            guangdu.append([suanfa_1,y])
        else:
            break
    for y in range(suanfa_2, -1,-1):
        if result[suanfa_1][y] == max_xx:
            guangdu.append([suanfa_1,y])
        else:
            break
    return guangdu
#拐点
def digui_fenjie(suanfa_1, suanfa_2, suanfa_3, suanfa_4):
    if suanfa_1 == suanfa_3 or suanfa_2 == suanfa_4:
        if zhilian_panduan(suanfa_1, suanfa_2, suanfa_3,suanfa_4):
            mouse_what_click(suanfa_1, suanfa_2, suanfa_3,suanfa_4)
            result[suanfa_1][suanfa_2] = max_xx
            result[suanfa_3][suanfa_4] = max_xx
        else:
            for guangdu_i in range(len(guangdu_panduan(suanfa_1,suanfa_2))):
                if yizhe_panduan(guangdu_panduan(suanfa_1,suanfa_2)[guangdu_i][0],guangdu_panduan(suanfa_1,suanfa_2)[guangdu_i][1],suanfa_3,suanfa_4):
                    print(guangdu_panduan(suanfa_1,suanfa_2)[guangdu_i][0],guangdu_panduan(suanfa_1,suanfa_2)[guangdu_i][1],suanfa_3,suanfa_4)
                    mouse_what_click(suanfa_1, suanfa_2, suanfa_3,suanfa_4)
                    result[suanfa_1][suanfa_2] = max_xx
                    result[suanfa_3][suanfa_4] = max_xx
                    break
    if suanfa_1 != suanfa_3 and suanfa_2 != suanfa_4:
        for guangdu_i in range(len(guangdu_panduan(suanfa_1, suanfa_2))):
            if yizhe_panduan(guangdu_panduan(suanfa_1, suanfa_2)[guangdu_i][0],guangdu_panduan(suanfa_1, suanfa_2)[guangdu_i][1], suanfa_3, suanfa_4):
                print(guangdu_panduan(suanfa_1, suanfa_2)[guangdu_i][0], guangdu_panduan(suanfa_1, suanfa_2)[guangdu_i][1], suanfa_3, suanfa_4)
                mouse_what_click(suanfa_1, suanfa_2, suanfa_3,suanfa_4)
                result[suanfa_1][suanfa_2] = max_xx
                result[suanfa_3][suanfa_4] = max_xx
                break
#模拟鼠标
def mouse_move(x,y):
    windll.user32.SetCursorPos(x,y)
#鼠标移动到坐标点击
def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.uni = random.uniform(0.4,0.8)
        time.sleep(time.uni)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_what_click(suanfa_1,suanfa_2,suanfa_3,suanfa_4):
    game_rect = win32gui.GetWindowRect(hwnd)
    mouse_click(game_rect[0] + 15 + suanfa_2 * 31, game_rect[1] + 189 + suanfa_1 * 35 )
    mouse_click(game_rect[0] + 15 + suanfa_4 * 31, game_rect[1] + 189 + suanfa_3 * 35 )



global hwnd
hwnd = win32gui.FindWindow("#32770","QQ游戏 - 连连看角色版")
if not hwnd:
    print("window not found!")
else:
    print(hwnd)
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(1)
game_rect = win32gui.GetWindowRect(hwnd)
#src_image = ImageGrab.grab((game_rect[0]+15,game_rect[1]+183,game_rect[0]+602,game_rect[1]+566))
src_image = ImageGrab.grab((game_rect[0]+15,game_rect[1]+181,game_rect[0]+602,game_rect[1]+566))
#裁剪并截图并命名
width = 589//31
hight = 385//35
result = zeros((hight, width))
image_list = []
i = 0
for col in range(0,hight):
    for row in range(0,width):
        clip_box = (row * 31+1, col * 35+4,(row + 1) * 31 - 5 ,(col + 1) * 35-2)
        image_list.insert(i,src_image.crop(clip_box))
        i += 1
        #center_image = src_image.crop(clip_box)
#比较图片，并命名同样的图片
poor = []
xx = 1
for bijiao_1 in range(len(image_list)):
    if result[bijiao_1 // 19][bijiao_1 % 19] not in poor:
        result[bijiao_1 // 19][bijiao_1 % 19] = int(xx)
    else:
        continue
    for bijiao_2 in range(bijiao_1+1,len(image_list)):
        clip_diff = image_compare(image_list[bijiao_1],image_list[bijiao_2])
        if sum(clip_diff) <= 600:
            result[bijiao_2 // 19][bijiao_2 % 19] = int(xx)
    poor.insert(xx-1,xx)
    xx += 1
print(poor)
print(len(image_list))
#print(image_list)
#把空白部分去掉
zidian_1 = {}
for items_1 in range(11):
    for items_2 in range(19):
        zidian_1[result[items_1][items_2]] = zidian_1.get(result[items_1][items_2], 0) + 1
items_3 = list(zidian_1.items())
items_3.sort(key=lambda x:x[1],reverse=True)
global max_xx
max_xx,count = items_3[0]
#输出连连看情况
for print_shu_col in range(11):
    #print(int(result[print_shu_col][print_shu_1]),end=" ")
    #print("{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}".format(int(result[print_shu_col][0]),int(result[print_shu_col][1]),int(result[print_shu_col][2]),int(result[print_shu_col][3]),int(result[print_shu_col][4]),int(result[print_shu_col][5]),int(result[print_shu_col][6]),int(result[print_shu_col][7]),int(result[print_shu_col][8]),int(result[print_shu_col][9]),int(result[print_shu_col][10]),int(result[print_shu_col][11]),int(result[print_shu_col][12]),int(result[print_shu_col][13]),int(result[print_shu_col][14]),int(result[print_shu_col][15]),int(result[print_shu_col][16]),int(result[print_shu_col][17]),int(result[print_shu_col][18]),))
    print("{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}".format(" " if int(result[print_shu_col][0]) == max_xx else int(result[print_shu_col][0])," " if int(result[print_shu_col][1]) == max_xx else int(result[print_shu_col][1])," " if int(result[print_shu_col][2]) == max_xx else int(result[print_shu_col][2])," " if int(result[print_shu_col][3]) == max_xx else int(result[print_shu_col][3])," " if int(result[print_shu_col][4]) == max_xx else int(result[print_shu_col][4])," " if int(result[print_shu_col][5]) == max_xx else int(result[print_shu_col][5])," " if int(result[print_shu_col][6]) == max_xx else int(result[print_shu_col][6])," " if int(result[print_shu_col][7]) == max_xx else int(result[print_shu_col][7])," " if int(result[print_shu_col][8]) == max_xx else int(result[print_shu_col][8])," " if int(result[print_shu_col][9]) == max_xx else int(result[print_shu_col][9])," " if int(result[print_shu_col][10]) == max_xx else int(result[print_shu_col][10])," " if int(result[print_shu_col][11]) == max_xx else int(result[print_shu_col][11])," " if int(result[print_shu_col][12]) == max_xx else int(result[print_shu_col][12])," " if int(result[print_shu_col][13]) == max_xx else int(result[print_shu_col][13])," " if int(result[print_shu_col][14]) == max_xx else int(result[print_shu_col][14])," " if int(result[print_shu_col][15]) == max_xx else int(result[print_shu_col][15])," " if int(result[print_shu_col][16]) == max_xx else int(result[print_shu_col][16])," " if int(result[print_shu_col][17]) == max_xx else int(result[print_shu_col][17])," " if int(result[print_shu_col][18]) == max_xx else int(result[print_shu_col][18])))




#-----------------------判断怎么才可以结合----------------------------
#算法部分
chongxin = True
while chongxin:
    for suanfa_1 in range(11):
        for suanfa_2 in range(19):
            if result[suanfa_1][suanfa_2] == max_xx:
                continue
            for suanfa_3 in range(11):
                for suanfa_4 in range(19):
                    if result[suanfa_3][suanfa_4] == result[suanfa_1][suanfa_2] and result[suanfa_1][suanfa_2] != max_xx:
                        #开始DFS算法
                        digui_fenjie(suanfa_1,suanfa_2,suanfa_3,suanfa_4)
                        #zuji_1 = []
    for suanfa_1 in range(11):
        for suanfa_2 in range(19):
            if result[suanfa_1][suanfa_2] == max_xx:
                continue
                chongxin = False
            else:
                chongxin = True
            for print_shu_col in range(11):
                # print(int(result[print_shu_col][print_shu_1]),end=" ")
                # print("{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}".format(int(result[print_shu_col][0]),int(result[print_shu_col][1]),int(result[print_shu_col][2]),int(result[print_shu_col][3]),int(result[print_shu_col][4]),int(result[print_shu_col][5]),int(result[print_shu_col][6]),int(result[print_shu_col][7]),int(result[print_shu_col][8]),int(result[print_shu_col][9]),int(result[print_shu_col][10]),int(result[print_shu_col][11]),int(result[print_shu_col][12]),int(result[print_shu_col][13]),int(result[print_shu_col][14]),int(result[print_shu_col][15]),int(result[print_shu_col][16]),int(result[print_shu_col][17]),int(result[print_shu_col][18]),))
                print("{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}{:3}".format(
                    " " if int(result[print_shu_col][0]) == max_xx else int(result[print_shu_col][0]),
                    " " if int(result[print_shu_col][1]) == max_xx else int(result[print_shu_col][1]),
                    " " if int(result[print_shu_col][2]) == max_xx else int(result[print_shu_col][2]),
                    " " if int(result[print_shu_col][3]) == max_xx else int(result[print_shu_col][3]),
                    " " if int(result[print_shu_col][4]) == max_xx else int(result[print_shu_col][4]),
                    " " if int(result[print_shu_col][5]) == max_xx else int(result[print_shu_col][5]),
                    " " if int(result[print_shu_col][6]) == max_xx else int(result[print_shu_col][6]),
                    " " if int(result[print_shu_col][7]) == max_xx else int(result[print_shu_col][7]),
                    " " if int(result[print_shu_col][8]) == max_xx else int(result[print_shu_col][8]),
                    " " if int(result[print_shu_col][9]) == max_xx else int(result[print_shu_col][9]),
                    " " if int(result[print_shu_col][10]) == max_xx else int(result[print_shu_col][10]),
                    " " if int(result[print_shu_col][11]) == max_xx else int(result[print_shu_col][11]),
                    " " if int(result[print_shu_col][12]) == max_xx else int(result[print_shu_col][12]),
                    " " if int(result[print_shu_col][13]) == max_xx else int(result[print_shu_col][13]),
                    " " if int(result[print_shu_col][14]) == max_xx else int(result[print_shu_col][14]),
                    " " if int(result[print_shu_col][15]) == max_xx else int(result[print_shu_col][15]),
                    " " if int(result[print_shu_col][16]) == max_xx else int(result[print_shu_col][16]),
                    " " if int(result[print_shu_col][17]) == max_xx else int(result[print_shu_col][17]),
                    " " if int(result[print_shu_col][18]) == max_xx else int(result[print_shu_col][18])))

























