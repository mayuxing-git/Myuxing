from keys import do, ctrl, shift
import time
from mss import mss
from window_impl import get_handinput_cand_area
import cv2
import numpy as np
import threading
from config import PARAMS, INPUT
from multiprocessing import Process

sct = mss()
first_cand_area = None


class Get_Handinput_Response_Time(threading.Thread):
    def __init__(self, start_time, handinput_mode):
        threading.Thread.__init__(self)
        self.start_time = start_time
        self.handinput_mode = handinput_mode
        self.cand_time = 0
        self.hash_value = 0

    def run(self):
        self.cand_time, self.hash_value = get_handinput_cand_time(self.start_time, self.handinput_mode)

    def get_result(self):
        return self.cand_time, self.hash_value


def aHash(img, pixel_x=40, pixel_y=40):
    # resize为30*30
    img = cv2.resize(img, (pixel_x, pixel_y), interpolation=cv2.INTER_CUBIC)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(pixel_x):
        for j in range(pixel_y):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / (pixel_x * pixel_y)
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(pixel_x):
        for j in range(pixel_y):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# Hash值对比
def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    if n > 20:
        return True, n
    else:
        return False, n


def similarity_judge(begin_time, img_list):
    a = time.time()
    img_list_size = len(img_list)
    # print('img_list size: ', img_list_size)
    left_img_num = 0
    right_img_num = img_list_size - 1
    is_cand_change = False
    while left_img_num != right_img_num - 1:
        mid = (right_img_num + left_img_num) // 2
        # print(mid)
        is_cand_change, hash_value = cmpHash(aHash(np.array(img_list[left_img_num])), aHash(np.array(img_list[mid])))
        if is_cand_change:
            right_img_num = mid
        else:
            left_img_num = mid
    # print('end loop:', right_img_num)
    is_cand_change, hash_value = cmpHash(aHash(np.array(img_list[left_img_num])), aHash(np.array(img_list[right_img_num])))
    if is_cand_change:
        find_cand_time = begin_time + (2 / img_list_size) * (right_img_num + 2)
        return find_cand_time, hash_value
    else:
        return begin_time + 300, hash_value
    # for i in range(img_list_size):
    #     is_cand_change, hash_value = cmpHash(aHash(np.array(img_list[i])), aHash(np.array(img_list[i + 1])))
    #     if is_cand_change:
    #         find_cand_time = begin_time + 3 / len(img_list) * (i + 2)
    #         print('similarity_judge cost time: ', time.time() - a)
    #         return find_cand_time, hash_value
    # print('similarity_judge cost time: ', time.time() - a)
    # return begin_time + 300, hash_value


def get_handinput_cand_time(start_time, handinput_mode):
    global first_cand_area
    if not first_cand_area:
        handarea_left, handarea_top, handarea_right, handarea_bottom = get_handinput_cand_area(handinput_mode)
        first_cand_area = {'top': handarea_top, 'left': handarea_left,
                           'width': handarea_right - handarea_left, 'height': handarea_bottom - handarea_top}
    handinput_area_img_list = []
    while time.time() - start_time < 2:
        handinput_area_img_list.append(sct.grab(first_cand_area))
        time.sleep(PARAMS[INPUT]['handinput_grab_time_interval'])
    find_cand_time, hash_value = similarity_judge(start_time, handinput_area_img_list)
    return find_cand_time - start_time, hash_value
