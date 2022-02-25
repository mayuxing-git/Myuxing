import os
import psutil
from config import M, INPUT
from config import PARAMS
from window_impl import get_virtual_keyboard_geometry, get_handinput_cand_area, get_handinput_window, \
    get_cand_virtual_keyboard_geometry
import time
from keys import do, space, Enter, BackSpace, ctrl, shift

str9key = '123456789'
str26key = 'qwertyuiopasdfghjklzxcvbnm'
virtual_keyboard_info = PARAMS['sogou']['virtual_keyboard']
pinyin_26key_btn_pos_info = virtual_keyboard_info['pinyin_26key_btn_pos_info']
pinyin_9key_btn_pos_info = virtual_keyboard_info['pinyin_9key_btn_pos_info']
keyboard_layout = {}
handinput_area_right = None
handinput_area_left = None
handinput_area_top = None
handinput_area_bottom = None


def get_process_info(proc):
    # 列出当前所有进程id
    pids = psutil.pids()
    pid = None
    for p in pids:
        try:
            if psutil.Process(p).name() == proc:
                pid = psutil.Process(p).pid
                break
        except:
            pass
    return pid


def start_edit(proc):
    # 开启进程
    os.popen(proc)
    time.sleep(2)


def close_edit(proc):
    # 关闭进程
    pid = get_process_info(proc)
    cmd = "kill -9 " + str(pid)
    os.popen(cmd)


def key_input(pinyin):
    if not pinyin or pinyin == '':
        return 0
    if pinyin == '*':
        do(BackSpace)
        time.sleep(0.01)
        return 0
    elif pinyin == '#':
        do(Enter)
        time.sleep(0.01)
        return 0
    elif pinyin == '&':
        do(space)
        time.sleep(0.01)
        return 0
    else:
        do(pinyin)
        time.sleep(0.01)
        return 1


def delete_pinyin(pinyin):
    if not pinyin or pinyin == '':
        return
    else:
        for i in range(0, len(pinyin)):
            do(BackSpace)
            time.sleep(0.01)


def ctrl_shift():
    do(ctrl + shift)
    time.sleep(1)


def init_virtualkey_layout():
    global keyboard_layout
    for key in virtual_keyboard_info:
        if key == 'pinyin_9key_btn_pos_info':
            keyPosInfo = virtual_keyboard_info['pinyin_9key_btn_pos_info']
            keyNameStr = str9key
            interval = keyPosInfo['interval']
            keyBtnPos = keyPosInfo['key_btn_pos']
            lastPosX, lastPosY = 0, 0
            for i in range(len(keyNameStr)):
                keyName = keyNameStr[i]
                if keyName not in keyBtnPos:
                    btn_coord = (lastPosX + interval, lastPosY)
                else:
                    btn_coord = keyBtnPos[keyName]
                lastPosX = btn_coord[0]
                lastPosY = btn_coord[1]
                keyboard_layout[keyName] = btn_coord
        elif key == 'pinyin_26key_btn_pos_info':
            keyPosInfo = virtual_keyboard_info['pinyin_26key_btn_pos_info']
            keyNameStr = str26key
            interval = keyPosInfo['interval']
            keyBtnPos = keyPosInfo['key_btn_pos']
            lastPosX, lastPosY = 0, 0
            for i in range(len(keyNameStr)):
                keyName = keyNameStr[i]
                if keyName not in keyBtnPos:
                    btn_coord = (lastPosX + interval, lastPosY)
                else:
                    btn_coord = keyBtnPos[keyName]
                lastPosX = btn_coord[0]
                lastPosY = btn_coord[1]
                keyboard_layout[keyName] = btn_coord
        else:
            keyboard_layout[key] = virtual_keyboard_info[key]


def virtualkey_click_event(key_name, box):
    click_button = (int(box.x + box.width * keyboard_layout[key_name][0]),
                    int(box.y + box.height * keyboard_layout[key_name][1]))
    M.click(click_button[0], click_button[1])


def virtualkey_input(pinyin, keyboardtype):
    if not pinyin or pinyin == '':
        return 0
    box = get_virtual_keyboard_geometry('Sogou')
    if pinyin == '*':
        virtualkey_click_event('backspace_' + str(keyboardtype), box)
        time.sleep(0.005)
        return 0
    elif pinyin == '#':
        virtualkey_click_event('enter_' + str(keyboardtype), box)
        time.sleep(0.005)
        return 0
    elif pinyin == '&':
        # virtualkey_click_event('Space_' + str(keyboardtype), box)
        time.sleep(0.005)
        return 2
    else:
        for i in range(0, len(pinyin)):
            virtualkey_click_event(pinyin[i], box)
            time.sleep(0.005)
        return 1


def virtualkey_delete_pinyin(pinyin, keyboardtype):
    if not pinyin or pinyin == '':
        return
    else:
        box = get_virtual_keyboard_geometry('Sogou')
        for i in range(0, len(pinyin)):
            virtualkey_click_event('backspace_' + str(keyboardtype), box)
            time.sleep(0.01)


def virtualkey_switch_keyboardtype(keyboard_type):
    box = get_virtual_keyboard_geometry('Sogou')
    virtualkey_click_event('switch_keyboard')
    time.sleep(1)
    if str(keyboard_type).endswith('key'):
        virtualkey_click_event(keyboard_type, box)
    else:
        virtualkey_click_event(str(keyboard_type) + 'key', box)
    time.sleep(1)


def virtualkey_click_first_cand(name='Sogou'):
    cand_area = get_cand_virtual_keyboard_geometry(name)
    width = cand_area.width
    height = cand_area.height
    posX = PARAMS['sogou']['virtual_keyboard']['first_cand_pos']
    click_btn = (int(cand_area[0] + width * posX), int(cand_area[1] + height / 2))
    M.click(click_btn[0], click_btn[1])


def init_layout():
    global keyboard_layout
    for key in PARAMS[INPUT]:
        keyboard_layout[key] = PARAMS[INPUT][key]


def init_handinput_area(handinput_mode):
    global handinput_area_top, handinput_area_bottom, handinput_area_left, handinput_area_right
    if not keyboard_layout:
        init_layout()
    if not handinput_area_top or not handinput_area_bottom or not handinput_area_left or not handinput_area_right:
        box = get_handinput_window()
        if INPUT == 'sogou':
            handinput_area_top = int(box.y + box.height * keyboard_layout['handinput_area']['top'])
            handinput_area_bottom = int(box.y + box.height * keyboard_layout['handinput_area']['bottom'])
            handinput_area_left = int(box.x + box.width * keyboard_layout['handinput_area']['left'])
            handinput_area_right = int(box.x + box.width * keyboard_layout['handinput_area']['right'])
        elif INPUT == 'xunfei':
            if handinput_mode == 'single_word_handinput':
                handinput_area_top = int(box.y + box.height * keyboard_layout['single_word_handinput_area']['top'])
                handinput_area_bottom = int(box.y + box.height * keyboard_layout['single_word_handinput_area']['bottom'])
                handinput_area_left = int(box.x + box.width * keyboard_layout['single_word_handinput_area']['left'])
                handinput_area_right = int(box.x + box.width * keyboard_layout['single_word_handinput_area']['right'])
            elif handinput_mode == 'multi_word_handinput':
                handinput_area_top = int(box.y + box.height * keyboard_layout['multi_word_handinput_area']['top'])
                handinput_area_bottom = int(box.y + box.height * keyboard_layout['multi_word_handinput_area']['bottom'])
                handinput_area_left = int(box.x + box.width * keyboard_layout['multi_word_handinput_area']['left'])
                handinput_area_right = int(box.x + box.width * keyboard_layout['multi_word_handinput_area']['right'])


def handinput(input_list, handinput_mode='single_word_handinput'):
    input_length = len(input_list)
    if input_length == 0:
        return False
    if not handinput_area_top or not handinput_area_bottom or not handinput_area_left or not handinput_area_right:
        init_handinput_area(handinput_mode)
    isneedScaled = False
    ispress = False
    x_pre = 0
    y_pre = 0
    # 坐标归一化
    tMinX, tMaxX, tMinY, tMaxY = 10000, 0, 10000, 0
    for i in range(input_length):
        tPoint = input_list[i]
        if tPoint[0] == -1:
            continue
        if tMinX > tPoint[0]:
            tMinX = tPoint[0]
        if tMaxX < tPoint[0]:
            tMaxX = tPoint[0]
        if tMinY > tPoint[1]:
            tMinY = tPoint[1]
        if tMaxY < tPoint[1]:
            tMaxY = tPoint[1]
    tDisX = tMaxX - tMinX
    tDisY = tMaxY - tMinY
    singleword = []

    tScaleX, tScaleY = 0, 0
    if tDisX:
        tScaleX = float((handinput_area_right - handinput_area_left) / tDisX)
    if tDisY:
        tScaleY = float((handinput_area_bottom - handinput_area_top) / tDisY)
    if tScaleX > tScaleY:
        tScale = tScaleY
    else:
        tScale = tScaleX
    if tScale < 1.0:
        isneedScaled = True
    if isneedScaled:
        for i in range(input_length):
            singlePoint = []
            tPoint = input_list[i]
            if tPoint[0] == -1:
                singlePoint.append(tPoint[0])
                singlePoint.append(tPoint[1])
                singleword.append(singlePoint)
                continue
            tPointX = int(tMinX + (tPoint[0] - tMinX) * tScale)
            tPointY = int(tMinY + (tPoint[1] - tMinY) * tScale)
            singlePoint.append(tPointX)
            singlePoint.append(tPointY)
            singleword.append(singlePoint)
    if isneedScaled:
        tMinX, tMaxX, tMinY, tMaxY = 10000, 0, 10000, 0
        for i in range(input_length):
            tPoint = singleword[i]
            if tPoint[0] == -1:
                continue
            if tMinX > tPoint[0]:
                tMinX = tPoint[0]
            if tMaxX < tPoint[0]:
                tMaxX = tPoint[0]
            if tMinY > tPoint[1]:
                tMinY = tPoint[1]
            if tMaxY < tPoint[1]:
                tMaxY = tPoint[1]
    toffsetX = int(handinput_area_left - tMinX)
    toffsetY = int(handinput_area_top - tMinY)
    scaled_inputlist = []
    for i in range(input_length):
        scaled_point = []
        tPointX, tPointY = 0, 0
        tPoint = []
        if isneedScaled:
            tPoint = singleword[i]
        else:
            tPoint = input_list[i]
        if tPoint[0] == -1:
            scaled_point.append(tPoint[0])
            scaled_point.append(tPoint[1])
            scaled_inputlist.append(scaled_point)
            continue
        tPointX = tPoint[0] + toffsetX
        tPointY = tPoint[1] + toffsetY
        scaled_point.append(tPointX)
        scaled_point.append(tPointY)
        scaled_inputlist.append(scaled_point)

    # 手写输入
    for i in range(input_length):
        tmp_first_point = scaled_inputlist[i]
        x = tmp_first_point[0]
        y = tmp_first_point[1]
        if x == -1 and y == 0:
            # Mouse click up
            M.release(x_pre, y_pre)
            time.sleep(0.005)
            ispress = False
        elif y != -1:
            x_pre = x
            y_pre = y
            if not ispress:
                # Mouse click down
                M.press(x, y)
                time.sleep(0.005)
                ispress = True
            else:
                # Mouse click move
                M.press(x, y)
                time.sleep(0.005)
    return True


# 通过候选索引index计算需点击候选的位置
def click_handinput_cand(index):
    box = get_handinput_cand_area()
    y_pos = int(box[3] - (box[3] - box[1]) / 5)
    interval = PARAMS[INPUT]['interval']
    if index == 1:
        x_pos = box[0] + int(interval / 2) + (index - 1) * interval
    else:
        x_pos = box[0] + int(interval / 2) + 2 * interval
    M.click(x_pos, y_pos)


def click_xunfei_handinput_cand(handinput_mode, index):
    box = get_handinput_cand_area(handinput_mode)
    if handinput_mode == 'multi_word_handinput':
        y_pos = int(box[1] + (box[3] - box[1]) / 2)
        if index == 1:
            x_pos = int(box[0] + (box[2] - box[0]) / 24)
        else:
            x_pos = int(box[0] + ((box[2] - box[0]) / 24) * 7)
    elif handinput_mode == 'single_word_handinput':
        cand_area_height_interval = int((box[3] - box[1]) / 3)
        cand_area_width_interval = int((box[2] - box[0]) / 3)
        y_pos = int(box[1] + cand_area_height_interval / 2)
        if index == 1:
            x_pos = int(box[0] + cand_area_width_interval / 2)
        else:
            x_pos = int(box[0] + 5 * (cand_area_width_interval / 2))
    M.click(x_pos, y_pos)


if __name__ == '__main__':
    init_virtualkey_layout()
