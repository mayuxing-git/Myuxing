import os
import psutil
from config import M
from config import PARAMS
from window_impl import get_sogou_virtualkeyboard_window, get_virtualkeyboard_candarea
import time
from keys import do, space, Enter, BackSpace, ctrl, shift

str9key = '123456789'
str26key = 'qwertyuiopasdfghjklzxcvbnm'
sogou_virtual_keyboard_info = PARAMS['sogou_virtual_keyboard']
pinyin_26key_btn_pos_info = sogou_virtual_keyboard_info['pinyin_26key_btn_pos_info']
pinyin_9key_btn_pos_info = sogou_virtual_keyboard_info['pinyin_9key_btn_pos_info']
keyboard_layout = {}


def get_process_info(proc):
    pids = psutil.pids()
    pid = None
    for p in pids:
        try:
            p_name = psutil.Process(p)
            if p_name.name() == proc:
                pid = p_name.pid
                break
        except:
            pass
    return pid


def start_edit(proc):
    os.popen(proc)
    time.sleep(2)


def close_edit(proc):
    pid = get_process_info(proc)
    if pid:
        try:
            cmd = "kill -9 " + str(pid)
            os.popen(cmd)
        except:
            pass


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
        pinyin = pinyin.lower()
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
    do(space)


def ctrl_shift():
    do(ctrl+shift)
    time.sleep(1)


def init_virtualkey_layout():
    global keyboard_layout
    for key in sogou_virtual_keyboard_info:
        if key == 'pinyin_9key_btn_pos_info':
            keyPosInfo = sogou_virtual_keyboard_info['pinyin_9key_btn_pos_info']
            keyNameStr = str9key
            interval = keyPosInfo['interval']
            keyBtnPos = keyPosInfo['key_btn_pos']
            lastPosX, lastPosY = 0, 0
            for i in range(len(keyNameStr)):
                single_btn = {}
                keyName = keyNameStr[i]
                if keyName not in keyBtnPos:
                    btn_coord = (lastPosX + interval, lastPosY)
                else:
                    btn_coord = keyBtnPos[keyName]
                lastPosX = btn_coord[0]
                lastPosY = btn_coord[1]
                keyboard_layout[keyName] = btn_coord
        elif key == 'pinyin_26key_btn_pos_info':
            keyPosInfo = sogou_virtual_keyboard_info['pinyin_26key_btn_pos_info']
            keyNameStr = str26key
            interval = keyPosInfo['interval']
            keyBtnPos = keyPosInfo['key_btn_pos']
            lastPosX, lastPosY = 0, 0
            for i in range(len(keyNameStr)):
                single_btn = {}
                keyName = keyNameStr[i]
                if keyName not in keyBtnPos:
                    btn_coord = (lastPosX + interval, lastPosY)
                else:
                    btn_coord = keyBtnPos[keyName]
                lastPosX = btn_coord[0]
                lastPosY = btn_coord[1]
                keyboard_layout[keyName] = btn_coord
        else:
            keyboard_layout[key] = sogou_virtual_keyboard_info[key]


def virtualkey_click_event(key_name, box):
    # box = get_sogou_virtualkeyboard_window('Sogou')
    click_button = (int(box.x + box.width * keyboard_layout[key_name][0]),
                    int(box.y + box.height * keyboard_layout[key_name][1]))
    M.click(click_button[0], click_button[1])


def virtualkey_input(pinyin, keyboardtype):
    if not pinyin or pinyin == '':
        return 0
    box = get_sogou_virtualkeyboard_window('Sogou')
    if pinyin == '*':
        virtualkey_click_event('backspace_' + str(keyboardtype), box)
        time.sleep(0.01)
        return 0
    elif pinyin == '#':
        virtualkey_click_event('enter_' + str(keyboardtype), box)
        time.sleep(0.01)
        return 0
    elif pinyin == '&':
        # virtualkey_click_event('Space_' + str(keyboardtype), box)
        time.sleep(0.01)
        return 2
    else:
        if str(keyboardtype).endswith('eng'):
            for p in pinyin:
                if p.isupper():
                    virtualkey_click_event('shift_26', box)
                    time.sleep(0.005)
                    virtualkey_click_event(p.lower(), box)
                else:
                    virtualkey_click_event(p, box)
                    time.sleep(0.005)
            time.sleep(0.01)
        else:
            pinyin = pinyin.lower()
            for i in range(0, len(pinyin)):
                virtualkey_click_event(pinyin[i], box)
                time.sleep(0.005)
            time.sleep(0.01)
        return 1


def virtualkey_delete_pinyin(pinyin, keyboardtype):
    if not pinyin or pinyin == '':
        return
    else:
        box = get_sogou_virtualkeyboard_window('Sogou')
        for i in range(0, len(pinyin)):
            virtualkey_click_event('backspace_' + keyboardtype, box)
            time.sleep(0.005)


def virtualkey_click_cand(cand_list, index, name='Sogou'):
    cand_area = get_virtualkeyboard_candarea(name)
    width = cand_area[2] - cand_area[0]
    height = cand_area[3] - cand_area[1]
    posX = cand_list[index - 1]['pos']
    click_btn = (int(cand_area[0] + width * posX), int(cand_area[1] + height / 2))
    M.click(click_btn[0], click_btn[1])
    time.sleep(0.01)


def virtualkey_switch_keyboardtype(keyboard_type):
    box = get_sogou_virtualkeyboard_window('Sogou')
    virtualkey_click_event('switch_keyboard', box)
    time.sleep(1)
    if str(keyboard_type).endswith('key'):
        virtualkey_click_event(keyboard_type, box)
    elif str(keyboard_type).startswith('26') and str(keyboard_type).endswith('eng'):
        virtualkey_click_event('26key_eng', box)
    else:
        virtualkey_click_event(str(keyboard_type) + 'key', box)
    time.sleep(1)
