from collections import namedtuple
import Xlib
import Xlib.display
import time
import numpy as np
import json
import requests
from config import INPUT, PARAMS
from mss import mss
from keys import do, space
# from PIL import Image
# import matplotlib.pyplot as plt
#
# import cv2
sct = mss()
MyGeom = namedtuple('MyGeom', 'x y height width')
handinput_window = None
status_window = None
disp = None
root = None
query = None
hand_default_box = None  # 手写框左上角坐标及长宽
status_default_box = None  # 搜狗悬浮窗


def get_root_screen():
    disp = Xlib.display.Display()
    root = disp.screen().root
    query = root.query_tree()
    return disp, root, query


def get_handinput_child_window(query):
    ids = []
    for window in query.children:
        # name = window.get_wm_name()
        # print(name, window.id)
        ids.append(window.id)
    return ids


def get_child_window(query, child_name):
    ids = []
    if child_name == 'Sogou':
        for window in query.children:
            name = window.get_wm_name()
            if name:
                if name.startswith(child_name):
                    # print(name, window.id)
                    ids.append(window.id)
    elif child_name == 'xunfei':
        for window in query.children:
            name = window.get_wm_name()
            if name:
                if name == PARAMS[INPUT]['status_window_name']:
                    # print(name, window.id)
                    ids.append(window.id)
                    break
    return ids


def get_active_window(disp, win_id):
    try:
        return disp.create_resource_object('window', win_id)
    except Xlib.error.XError:
        print("[Debug]get_active_window error, win_id: " + str(win_id))


def get_absolute_geometry(root, win):
    """
    Returns the (x, y, height, width) of a window relative to the top-left
    of the screen.
    """
    geom = win.get_geometry()
    (x, y) = (geom.x, geom.y)
    while True:
        parent = win.query_tree().parent
        pgeom = parent.get_geometry()
        x += pgeom.x
        y += pgeom.y
        if parent.id == root.id:
            break
        win = parent
    return MyGeom(x, y, geom.height, geom.width)


def get_window_box(root, win):
    """
    Returns (x1, y1, x2, y2) relative to the top-left of the screen.
    """
    geom = get_absolute_geometry(root, win)
    """
    x1 = geom.x
    y1 = geom.y
    x2 = x1 + geom.width
    y2 = y1 + geom.height
    """
    x1 = geom.x
    y1 = geom.y
    x2 = geom.x + geom.width
    y2 = geom.y + geom.height
    return MyGeom(x1, y1, x2, y2)


# 获取手写框的位置信息
def get_handinput_window():
    global disp, root, query, handinput_window, hand_default_box
    if not disp or not root or not query or not handinput_window:
        time.sleep(1)
        disp, root, query = get_root_screen()
        win_ids = get_handinput_child_window(query)
        for i in range(len(win_ids)):
            try:
                win = get_active_window(disp, win_ids[i])
                box = get_absolute_geometry(root, win)
                if INPUT == 'sogou':
                    #if box.height / box.width == 412 / 622:
                    if box.height / box.width == 430 / 553:#2.5手写
                        handinput_window = win_ids[i]
                        break
                elif INPUT == 'xunfei':
                    if box.height / box.width == 860 / 1240:
                        handinput_window = win_ids[i]
                        break
            except Xlib.error.BadWindow:
                print("Window vanished")
    win = get_active_window(disp, handinput_window)
    box = get_absolute_geometry(root, win)
    if not hand_default_box:
        hand_default_box = box
    return box


# 获取悬浮窗位置，为了调起手写输入
def get_status_window(name):
    global disp, root, query, status_default_box, status_window
    if not disp or not root or not query or not status_window:
        time.sleep(1)
        disp, root, query = get_root_screen()
        if name == 'sogou':
            win_ids = get_child_window(query, name.capitalize())
        else:
            win_ids = get_child_window(query, name)
        for i in range(len(win_ids)):
            try:
                win = get_active_window(disp, win_ids[i])
                box = get_absolute_geometry(root, win)
                if name == 'sogou':
                    #if box.width / box.height == 215 / 28:
                    if box.width / box.height == 192 / 29:
                    #if box.width / box.height == 215 / 28:#2.5
                        status_window = win_ids[i]
                        break
                elif name == 'xunfei':
                    if box.width / box.height == 400 / 56:
                        status_window = win_ids[i]
                        break
            except Xlib.error.BadWindow:
                print("Window vanished")
    win = get_active_window(disp, status_window)
    box = get_absolute_geometry(root, win)
    if not status_default_box:
        status_default_box = box
    return box


def get_handinput_cand_area(handinput_mode='single_word_handinput'):
    if not hand_default_box:
        get_handinput_window()
    if INPUT == 'sogou':
        handinput_area_top = int(hand_default_box.y + hand_default_box.height * PARAMS[INPUT]['candarea']['top'])
        handinput_area_bottom = int(hand_default_box.y + hand_default_box.height * PARAMS[INPUT]['candarea']['bottom'])
        handinput_area_left = int(hand_default_box.x + hand_default_box.width * PARAMS[INPUT]['candarea']['left'])
        handinput_area_right = int(hand_default_box.x + hand_default_box.width * PARAMS[INPUT]['candarea']['right'])
    elif INPUT == 'xunfei':
        if handinput_mode == 'single_word_handinput':
            handinput_area_top = int(hand_default_box.y + hand_default_box.height *
                                     PARAMS[INPUT]['single_word_candarea']['top'])
            handinput_area_bottom = int(hand_default_box.y + hand_default_box.height *
                                        PARAMS[INPUT]['single_word_candarea']['bottom'])
            handinput_area_left = int(hand_default_box.x + hand_default_box.width *
                                      PARAMS[INPUT]['single_word_candarea']['left'])
            handinput_area_right = int(hand_default_box.x + hand_default_box.width *
                                       PARAMS[INPUT]['single_word_candarea']['right'])
        elif handinput_mode == 'multi_word_handinput':
            handinput_area_top = int(hand_default_box.y + hand_default_box.height *
                                     PARAMS[INPUT]['multi_word_cand_area']['top'])
            handinput_area_bottom = int(hand_default_box.y + hand_default_box.height *
                                        PARAMS[INPUT]['multi_word_cand_area']['bottom'])
            handinput_area_left = int(hand_default_box.x + hand_default_box.width *
                                      PARAMS[INPUT]['multi_word_cand_area']['left'])
            handinput_area_right = int(hand_default_box.x + hand_default_box.width *
                                       PARAMS[INPUT]['multi_word_cand_area']['right'])
    return handinput_area_left, handinput_area_top, handinput_area_right, handinput_area_bottom


# 获取设置窗口位置
def get_sogou_configwindow():
    box = None
    disp, root, query = get_root_screen()
    NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
    config_win_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
    config_win = get_active_window(disp, config_win_id)
    box = get_absolute_geometry(root, config_win)
    return box


# 获取手写候选区图像并进行扩充
def get_and_expand_candarea_image():
    box = get_handinput_cand_area()
    cand_area = {'top': box[1], 'left': box[0],
                 'width': box[2] - box[0], 'height': box[3] - box[1]}
    candarea_width = cand_area['width']
    candarea_height = cand_area['height']
    src_image = np.array(sct.grab(cand_area))
    src_image = np.flip(src_image[:, :, :3], 2)
    interval = PARAMS[INPUT]['interval']
    dst_image = np.full((candarea_height, candarea_width + interval * PARAMS[INPUT]['handinput_default_cand_num'], 3),
                        255, dtype=np.uint8)
    for i in range(len(src_image)):
        cand_count = 0
        k = 0
        for j in range(len(src_image[i])):
            if j == cand_count * interval and cand_count <= PARAMS[INPUT]['handinput_default_cand_num'] - 1:
                for l in range(interval):
                    dst_image[i][k] = [255, 255, 255]
                    k += 1
                cand_count += 1
            dst_image[i][k] = src_image[i][j]
            k += 1
    return dst_image


def get_ocr_resultlist(handinput_mode='single_word_handinput'):
    if INPUT == 'sogou':
        image = np.array(get_and_expand_candarea_image())
        # image = cv2.resize(image, (200, 28))
        data = {'image': image.tolist()}
        response = requests.post('http://ai.qa.sogou/api/ocr/cand/numpy', json=data)
        ocr_result = response.text
        try:
            result_list = json.loads(ocr_result)
        except:
            return []
    elif INPUT == 'xunfei':
        box = get_handinput_cand_area(handinput_mode)
        if handinput_mode == 'single_word_handinput':
            result_list = list()
            image_list = list()
            cand_area_height_interval = int((box[3] - box[1]) / 3)
            ocr_result_list = []
            for i in range(3):
                cand_area = {'top': box[1] + i * cand_area_height_interval, 'left': box[0],
                             'width': box[2] - box[0], 'height': cand_area_height_interval}
                image = np.array(sct.grab(cand_area))
                image = np.flip(image[:, :, :3], 2)
                # image_list.append(image)

                data = {'image': image.tolist()}
                response = requests.post('http://ai.qa.sogou.com/api/ocr/cand/numpy', json=data)
                ocr_result = response.text
                try:
                    ocr_result_list.append(json.loads(ocr_result))
                except:
                    ocr_result_list.append([])
            for i in range(len(ocr_result_list)):
                if ocr_result_list[i]:
                    result_list += ocr_result_list[i]

            # image = None
            # for i in range(len(image_list)):
            #     if i == 0:
            #         image = image_list[i]
            #     else:
            #         image = np.concatenate((image, image_list[i]), axis=1)
            # data = {'image': image.tolist()}
            # response = requests.post('http://ai.qa.sogou.com/api/ocr/cand/numpy', json=data)
            # ocr_result = response.text
            # try:
            #     result_list = json.loads(ocr_result)
            # except:
            #     result_list = []
            # pass
        elif handinput_mode == 'multi_word_handinput':
            cand_area = {'top': box[1], 'left': box[0],
                         'width': box[2] - box[0], 'height': box[3] - box[1]}
            image = np.array(sct.grab(cand_area))
            image = np.flip(image[:, :, :3], 2)
            # plt.imshow(image)
            data = {'image': image.tolist()}
            response = requests.post('http://ai.qa.sogou.com/api/ocr/cand/numpy', json=data)
            ocr_result = response.text
            try:
                result_list = json.loads(ocr_result)
            except:
                return []
    return result_list


def clear_test_enviroment():
    global disp, root, query, handinput_window, hand_default_box, status_window, status_default_box
    disp, root, query = None, None, None
    handinput_window, hand_default_box = None, None
    status_window, status_default_box = None, None
