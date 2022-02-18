from collections import namedtuple
import Xlib
import Xlib.display
import time
import pyscreenshot
import numpy as np
import json
import requests
from config import INPUT, PARAMS, M
import psutil
from keys import do, space

# import cv2

MyGeom = namedtuple('MyGeom', 'x y height width')
status_win_id = None
virtual_keyboard_win_id = None
cand_win_id = None
cand_geom_for_perf = None
disp = None
root = None
query = None
sogou_handinput_id = None
hand_default_box = None
voiceinput_id = None
voice_default_box = None


def get_root_screen():
    disp = Xlib.display.Display()
    root = disp.screen().root
    query = root.query_tree()
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
    返回相对于左上角的窗口的(x, y，高度，宽度)的屏幕。
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


# 获取用于ocr的候选截图区域
def get_cand_box_coordinate(root, win):
    """
    相对于屏幕左上角返回(x1, y1, height, width)。
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
    return (x1, y1, x2, y2)


# 获取输入法状态栏的区域
def get_status_box_geometry(name):
    box = None
    if not name:
        return box
    global disp, root, query, status_win_id
    if not disp or not root or not query or not status_win_id:
        disp, root, query = get_root_screen()
        win_ids = get_child_window(query, name)
        for i in range(len(win_ids)):
            try:
                win = get_active_window(disp, win_ids[i])
                box = get_absolute_geometry(root, win)
                if name == 'Sogou':
                    #if box.width / box.height == 295 / 59:
                    if box.width / box.height == 215 / 28:
                        status_win_id = win_ids[i]
                        break
                elif name == 'xunfei':
                    if box.width / box.height == 400 / 56:
                        status_win_id = win_ids[i]
                        break
            except Xlib.error.BadWindow:
                print("Window vanished")
    if not box and status_win_id:  # todo 判断status_win_id不为空再返回box
        win = get_active_window(disp, status_win_id)
        box = get_absolute_geometry(root, win)
    return box


# 获取输入法候选的区域
def get_cand_box_geometry(name):
    box = None
    if not name:
        return box
    global disp, root, query, cand_win_id, cand_geom_for_perf
    if not disp or not root or not query or not cand_win_id:
        disp, root, query = get_root_screen()
        if name == 'Sogou':
            win_ids = get_child_window(query, name)
            box_max = 0
            for i in range(len(win_ids)):
                temp_cand_win_id = win_ids[i]
                time.sleep(0.05)
                win = get_active_window(disp, temp_cand_win_id)
                temp_box = get_absolute_geometry(root, win)
                if temp_box.height > box_max:
                    box_max = temp_box.height
                    cand_win_id = temp_cand_win_id
        elif name == 'xunfei':
            for window in query.children:
                win_id = window.id
                time.sleep(0.005)
                win = get_active_window(disp, win_id)
                temp_box = get_absolute_geometry(root, win)
                if temp_box.width != 0 and (temp_box.height / temp_box.width == 180 / 692 or                     temp_box.height / temp_box.width == 75 / 320):
                    cand_win_id = win_id
                    break
    if not cand_geom_for_perf and cand_win_id:
        win = get_active_window(disp, cand_win_id)
        cor = get_cand_box_coordinate(root, win)
        cand_geom_for_perf = MyGeom(cor[0], cor[1], cor[3] - cor[1], cor[2] - cor[0])
    return cand_geom_for_perf


# 获取手写框的区域
def get_handinput_window():
    global disp, root, query, sogou_handinput_id, hand_default_box
    if not disp or not root or not query or not sogou_handinput_id:
        disp, root, query = get_root_screen()
        win_ids = []
        for window in query.children:
            win_ids.append(window.id)
        for i in range(len(win_ids)):
            try:
                win = get_active_window(disp, win_ids[i])
                box = get_absolute_geometry(root, win)
                if INPUT == 'sogou':
                    #if box.height / box.width == 412 / 622 and box.x > 0:
                    if box.height / box.width == 430 / 553 and box.x > 0:#2.5手写
                        sogou_handinput_id = win_ids[i]
                        break
                elif INPUT == 'xunfei':
                    if box.height / box.width == 860 / 1240 and box.x > 0:
                        sogou_handinput_id = win_ids[i]
                        break
            except Xlib.error.BadWindow:
                print("Window vanished")
    if not hand_default_box:
        win = get_active_window(disp, sogou_handinput_id)
        box = get_absolute_geometry(root, win)
        hand_default_box = box
    return hand_default_box


def get_handinput_cand_area(handinput_mode='single_word_handinput'):
    if not hand_default_box:
        get_handinput_window()
    if INPUT == 'sogou':
        handinput_area_top = int(
            hand_default_box.y + hand_default_box.height * PARAMS[INPUT]['handinput_candarea']['top'])
        handinput_area_bottom = int(
            hand_default_box.y + hand_default_box.height * PARAMS[INPUT]['handinput_candarea']['bottom'])
        handinput_area_left = int(
            hand_default_box.x + hand_default_box.width * PARAMS[INPUT]['handinput_candarea']['left'])
        handinput_area_right = int(
            hand_default_box.x + hand_default_box.width * PARAMS[INPUT]['handinput_candarea']['right'])
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


def get_top_window():
    box = None
    disp, root, query = get_root_screen()
    NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
    win_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
    top_window = get_active_window(disp, win_id)
    box = get_absolute_geometry(root, top_window)
    return box


def get_first_on_screen_area():
    edit_window = get_top_window()
    edit_area_top = int(edit_window.y + edit_window.height *
                        PARAMS[INPUT]['editor_first_word']['top'])
    edit_area_bottom = int(edit_window.y + edit_window.height *
                           PARAMS[INPUT]['editor_first_word']['bottom'])
    edit_area_left = int(edit_window.x + edit_window.width *
                         PARAMS[INPUT]['editor_first_word']['left'])
    edit_area_right = int(edit_window.x + edit_window.width *
                          PARAMS[INPUT]['editor_first_word']['right'])
    return edit_area_left, edit_area_top, edit_area_right, edit_area_bottom


# 获取语音键盘的区域
def get_voiceinput_geometry():
    global disp, root, query, voiceinput_id, voice_default_box
    if not disp or not root or not query or not voiceinput_id:
        disp, root, query = get_root_screen()
        win_ids = []
        for window in query.children:
            win_ids.append(window.id)
        for i in range(len(win_ids)):
            try:
                win = get_active_window(disp, win_ids[i])
                box = get_absolute_geometry(root, win)
                if INPUT == 'sogou':
                    if box.height / box.width == 156 / 125 and box.x >= 0:
                        voiceinput_id = win_ids[i]
                        break
                elif INPUT == 'xunfei':
                    if box.height / box.width == 89 / 300 and box.x >= 0:
                        voiceinput_id = win_ids[i]
                        break
            except Xlib.error.BadWindow:
                print("Window vanished")
    if not voice_default_box:
        win = get_active_window(disp, voiceinput_id)
        box = get_absolute_geometry(root, win)
        voice_default_box = box
    return voice_default_box


# 获取虚拟键盘的区域
def get_virtual_keyboard_geometry(name):
    box = None
    if not name:
        return box
    global disp, root, query, virtual_keyboard_win_id
    if not disp or not root or not query or not virtual_keyboard_win_id:
        disp, root, query = get_root_screen()
        win_ids = get_child_window(query, name)
        box_max = 0
        for i in range(len(win_ids)):
            temp_virtual_keyboard_win_id = win_ids[i]
            time.sleep(0.05)
            win = get_active_window(disp, temp_virtual_keyboard_win_id)
            temp_box = get_absolute_geometry(root, win)
            if temp_box.height > box_max:
                box = temp_box
                box_max = temp_box.height
                virtual_keyboard_win_id = temp_virtual_keyboard_win_id
        # print(box)
    if not box and virtual_keyboard_win_id:
        win = get_active_window(disp, virtual_keyboard_win_id)
        box = get_absolute_geometry(root, win)
    return box


# 获取虚拟键盘候选的区域
def get_cand_virtual_keyboard_geometry(name):
    box = None
    if not name:
        return box
    box = get_virtual_keyboard_geometry(name)
    x1 = int(box.x)
    y1 = int(box.y + box.height * PARAMS[INPUT]['virtual_keyboard']['cand_area_top'])
    x2 = int(box.x + box.width * PARAMS[INPUT]['virtual_keyboard']['cand_area'][0])
    y2 = int(box.y + box.height * PARAMS[INPUT]['virtual_keyboard']['cand_area'][1])

    return MyGeom(x1, y1, y2 - y1, x2 - x1)


def get_ocr_resultlist(name):
    box = get_status_box_geometry(name)
    box = (box.x, box.y, box.x + box.width, box.y + box.height)
    image = pyscreenshot.grab(bbox=box)
    image.show()
    image.save('1.jpg')
    image = np.array(image)
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


def get_all_ime_pid(proc):
    pids = psutil.pids()
    pid = list()
    # for p in pids:
    #     p_name = psutil.Process(p)
    #     print(p, p_name.name())
    for p in pids:
        try:
            p_name = psutil.Process(p)
            if p_name.name().lower().startswith(proc):
                print(p_name.pid, p_name.name())
                pid.append(p)
        except:
            pass
    return pid


def get_ime_pid(ime_name):
    pid = []
    if ime_name == 'sogou':
        pid = get_all_ime_pid(ime_name)
    elif ime_name == 'xunfei':
        pid = get_all_ime_pid('ifly')
    return pid


def get_handinput_pid(proc):
    pids = psutil.pids()
    pid = list()
    # for p in pids:
    #     p_name = psutil.Process(p)
    #     print(p_name.pid, p_name.name())
    for p in pids:
        try:
            p_name = psutil.Process(p)
            if p_name.name() == proc:
                # print(p_name.pid, p_name.name())
                pid.append(p)
        except:
            pass
    return pid


if __name__ == '__main__':
    get_ocr_resultlist('Sogou')
