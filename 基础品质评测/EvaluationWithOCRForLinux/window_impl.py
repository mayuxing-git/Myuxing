from collections import namedtuple
import Xlib
import Xlib.display
import time
import pyscreenshot
import numpy as np
import json
import requests
from config import INPUT, PARAMS
from keys import do, space
from mss import mss

# import cv2

sct = mss()
MyGeom = namedtuple('MyGeom', 'x y height width')
cand_win_id = None
disp = None
root = None
query = None
default_box = None  # 后悬窗位置
status_default_box = None
status_window = None
mointor_width = None


def get_root_screen():
    global mointor_width
    disp = Xlib.display.Display()
    root = disp.screen().root
    query = root.query_tree()
    mointor_width = root.get_geometry().width
    return disp, root, query


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
    Returns (x, y, height, width) relative to the top-left of the screen.
    """
    geom = get_absolute_geometry(root, win)
    """
    x1 = geom.x
    y1 = geom.y
    x2 = x1 + geom.width
    y2 = y1 + geom.height
    """
    x1 = int(geom.x + geom.width * PARAMS[INPUT]['candarea']['left'])
    y1 = int(geom.y + geom.height * PARAMS[INPUT]['candarea']['top'])
    x2 = int(geom.x + geom.width * PARAMS[INPUT]['candarea']['right'])
    y2 = int(geom.y + geom.height * PARAMS[INPUT]['candarea']['bottom'])

    return MyGeom(x1, y1, y2 - y1, x2 - x1)


def get_status_window(name='Sogou'):
    global disp, root, query, status_default_box, status_window
    if not disp or not root or not query or not status_window:
        time.sleep(1)
        disp, root, query = get_root_screen()
        win_ids = get_child_window(query, name)
        for i in range(len(win_ids)):
            try:
                win = get_active_window(disp, win_ids[i])  # UI变化挑食
                box = get_absolute_geometry(root, win)
                if name == 'Sogou':
                    if box.width / box.height == 295 / 59:
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


# 获取用于ocr的截图区域-候选窗口
def get_box_coordinate(name):
    box = None
    temp_box = None
    if not name:
        return box
    global disp, root, query, cand_win_id, default_box
    if name == 'Sogou':
        if not disp or not root or not query or not cand_win_id:
            time.sleep(1)
            disp, root, query = get_root_screen()
            win_ids = get_child_window(query, name)
            box_height = 0
            for i in range(len(win_ids)):
                # if len(win_ids) > 0:
                # cand_win_id = win_ids[len(win_ids) - 1]
                temp_cand_win_id = win_ids[i]
                # time.sleep(0.05)
                win = get_active_window(disp, temp_cand_win_id)
                temp_box = get_window_box(root, win)
                if temp_box.height > box_height:
                    box = temp_box
                    box_height = temp_box.height
                    cand_win_id = temp_cand_win_id
            # print(box)
        if cand_win_id:
            time.sleep(0.05)
            win = get_active_window(disp, cand_win_id)
            box = get_window_box(root, win)
            if not default_box:
                default_box = get_absolute_geometry(root, win)
    elif name == 'xunfei':
        if not disp or not root or not query or not cand_win_id:
            time.sleep(1)
            disp, root, query = get_root_screen()
            for window in query.children:
                win_id = window.id
                # time.sleep(0.05)
                win = get_active_window(disp, win_id)
                temp_box = get_absolute_geometry(root, win)
                if temp_box.width != 0 and (temp_box.height / temp_box.width == 180 / 692 or
                                            temp_box.height / temp_box.width == 86 / 406 or
                                            temp_box.height / temp_box.width == 75 / 320):
                    box = temp_box
                    cand_win_id = win_id
                    break
        if cand_win_id:
            time.sleep(0.05)
            win = get_active_window(disp, cand_win_id)
            box = get_window_box(root, win)
            if not default_box:
                default_box = get_absolute_geometry(root, win)
    if box:
        return (box.x, box.y, box.x + box.width, box.y + box.height)
    else:
        return None


def open_xunfei_Property_setting_window():
    global disp, root, query
    if not disp or not root or not query:
        time.sleep(1)
        disp, root, query = get_root_screen()
    ids = []
    for window in query.children:
        ids.append(window.id)
    for i in range(len(ids)):
        win = get_active_window(disp, ids[i])
        temp_box = get_absolute_geometry(root, win)
        if temp_box.height / temp_box.width == 496 / 334:
            return temp_box
    return None


#
def get_default_cand_box():
    if cand_win_id:
        win = get_active_window(disp, cand_win_id)
        box = get_absolute_geometry(root, win)
    return box


def get_ocr_resultlist(name):
    box = get_box_coordinate(name)
    cand_area = {'top': box[1], 'left': box[0],
                 'width': box[2] - box[0], 'height': box[3] - box[1]}
    if cand_area['width'] > mointor_width - cand_area['left']:
        cand_area['width'] = int(mointor_width - cand_area['left'])
    # image = pyscreenshot.grab(bbox=box)
    # image.show()
    # image = np.array(pyscreenshot.grab(bbox=box))
    image = np.array(sct.grab(cand_area))
    image = np.flip(image[:, :, :3], 2)
    # image = cv2.resize(image, (200, 28))
    data = {'image': image.tolist()}
    response = requests.post('http://ai.qa.sogou/api/ocr/cand/numpy', json=data)
    ocr_result = response.text
    try:
        result_list = json.loads(ocr_result)
    except:
        return []
    # test_ocr = CnOcr()
    # result_list = test_ocr.ocr(image, True)[0]
    # print(result_list)
    return result_list


def get_configwindow():
    box = None
    disp, root, query = get_root_screen()
    NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
    config_win_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
    config_win = get_active_window(disp, config_win_id)
    box = get_absolute_geometry(root, config_win)
    return box


def return_default_box():
    box = get_default_cand_box()
    try_time = 0
    while try_time < 3:
        if box.height == default_box.height:
            return
        else:
            do(space)
            time.sleep(0.01)
        try_time += 1


def get_sogou_virtualkeyboard_window(name):
    box = None
    temp_box = None
    if not name:
        return box
    global disp, root, query, cand_win_id
    if not disp or not root or not query or not cand_win_id:
        time.sleep(1)
        disp, root, query = get_root_screen()
        win_ids = get_child_window(query, name)
        box_height = 0
        if len(win_ids) > 0:
            for i in range(len(win_ids)):
                temp_cand_win_id = win_ids[i]
                time.sleep(0.05)
                win = get_active_window(disp, temp_cand_win_id)
                temp_box = get_absolute_geometry(root, win)
                if temp_box.height - temp_box.y > box_height:
                    cand_win_id = temp_cand_win_id
                    box_height = temp_box.width - temp_box.y
    if cand_win_id:
        # time.sleep(0.05)
        win = get_active_window(disp, cand_win_id)
        box = get_absolute_geometry(root, win)
    return box


def get_virtualkeyboard_candarea(name):
    box = get_sogou_virtualkeyboard_window(name)
    x1 = int(box.x + box.width * PARAMS['sogou_virtual_keyboard']['candarea']['left'])
    y1 = int(box.y + box.height * PARAMS['sogou_virtual_keyboard']['candarea']['top'])
    x2 = int(box.x + box.width * PARAMS['sogou_virtual_keyboard']['candarea']['right'])
    y2 = int(box.y + box.height * PARAMS['sogou_virtual_keyboard']['candarea']['bottom'])

    return x1, y1, x2, y2


def threshold_image(src_image):
    for i in range(len(src_image)):
        for j in range(len(src_image[i])):
            if np.mean(src_image[i][j]) < 240:
                src_image[i][j] = [80, 80, 80]
    # 在候选区域前加一块空白
    # tmp_img = np.full((len(src_image), 100, 3), 255, dtype=np.uint8)
    # expand_img = np.hstack((tmp_img, src_image))
    # img1 = Image.fromarray(expand_img, 'RGB')
    # img1.show()
    return src_image


def get_virtualkeyboard_ocr_resultlist(name):
    box = get_virtualkeyboard_candarea(name)
    virtual_cand_area = {'top': box[1], 'left': box[0],
                         'width': box[2] - box[0], 'height': box[3] - box[1]}
    # image = np.array(pyscreenshot.grab(bbox=box))
    image = np.array(sct.grab(virtual_cand_area))
    image = np.flip(image[:, :, :3], 2)
    image_thresh = threshold_image(image)
    # GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # thd, image1 = cv2.threshold(GrayImage, 0, 255, cv2.THRESH_OTSU)
    # thd, image1 = cv2.threshold(GrayImage, 10, 255, cv2.THRESH_BINARY_INV)
    # image1 = np.array(image_thresh)
    # r, g, b = cv2.split(image)
    # image = cv2.resize(image, (200, 28))
    data = {'image': image_thresh.tolist()}
    response = requests.post('http://ai.qa.sogou/api/ocr/cand/numpy', json=data)
    # response = requests.post('http://10.129.20.188:8080/api/ocr/cand/numpy', json=data)
    ocr_result = response.text
    try:
        result_list = json.loads(ocr_result)
    except:
        return []
    if result_list:
        for i in range(len(result_list)):
            result_tobe_process_pre = result_list[i]['text']
            result_tobe_process = ''
            for j in range(len(result_tobe_process_pre)):
                if result_tobe_process_pre[j] == '—':
                    result_tobe_process += '一'
                else:
                    result_tobe_process += result_tobe_process_pre[j]
            result_list[i]['text'] = result_tobe_process
    return result_list
