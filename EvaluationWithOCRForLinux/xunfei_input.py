import time
import os
import re
from config import INPUT, PARAMS, M, EDIT
from window_impl import get_ocr_resultlist, get_configwindow, get_status_window, open_xunfei_Property_setting_window,\
    get_box_coordinate
from keys import do, Enter
from fake_input import start_edit, close_edit, key_input


# from cnocr import CnOcr


# 将ocr识别结果按照候选序号放入list
def get_xunfei_resultlist():
    ocr_resultlist = get_ocr_resultlist(INPUT)
    if ocr_resultlist:
        result_tobe_process_pre = ''
        for i in range(len(ocr_resultlist)):
            result_tobe_process_pre += ocr_resultlist[i]['text']
        result_tobe_process = ''
        for i in range(len(result_tobe_process_pre)):
            if result_tobe_process_pre[i] == '—':
                result_tobe_process += '一'
            else:
                result_tobe_process += result_tobe_process_pre[i]
        # result_tobe_process.replace(u"—", u"一")
        new_result = list()
        word = ''
        cand_count = 0
        cand_mark = False
        res_len = len(result_tobe_process)
        for i in range(len(result_tobe_process)):
            if cand_mark:
                cand_mark = False
                continue
            if cand_count == 0:
                cand_count += 1
                if result_tobe_process[0] == '1' or result_tobe_process[0] == 'l':
                    if result_tobe_process[1] == '.':
                        cand_mark = True
                elif result_tobe_process[0] == '.':
                    continue
                else:
                    word += result_tobe_process[0]
            elif result_tobe_process[i] == str(cand_count + 1) and i < (res_len - 1):
                if word != '':
                    word = re.sub(u"\\(.*?\\)", "", word)
                    new_result.append(word)
                    word = ''
                cand_count += 1
                if result_tobe_process[i + 1] == '.':
                    cand_mark = True
            else:
                word += result_tobe_process[i]
        if len(word) > 0:
            new_result.append(word)
        # print(new_result)
        return new_result
    else:
        return []


# def xunfeipinyin_dict_clear():
#     ime_position = get_status_window(name='xunfei')
#     get_config_button = (int(ime_position.x + ime_position.width * PARAMS[INPUT]['handinput_btn'][0]),
#                          int(ime_position.y + ime_position.height * PARAMS[INPUT]['handinput_btn'][1]))
#     M.click(get_config_button[0], get_config_button[1], button=2)
#     time.sleep(1)
#     open_config = open_xunfei_Property_setting_window()
#     if open_config:
#         open_config_button = (int(open_config.x + open_config.width * PARAMS[INPUT]['open_config_window'][0]),
#                               int(open_config.y + open_config.height * PARAMS[INPUT]['open_config_window'][1]))
#         M.click(open_config_button[0], open_config_button[1])
#     time.sleep(5)
#     box = get_configwindow()
#     # clear pinyin dict
#     xunfei_dict_button = (int(box.x + box.width * PARAMS[INPUT]['pinyin_dict_button'][0]),
#                           int(box.y + box.height * PARAMS[INPUT]['pinyin_dict_button'][1]))
#     M.click(xunfei_dict_button[0], xunfei_dict_button[1])
#     time.sleep(1)
#     xunfei_dict_clear = (int(box.x + box.width * PARAMS[INPUT]['pinyin_clear_button'][0]),
#                          int(box.y + box.height * PARAMS[INPUT]['pinyin_clear_button'][1]))
#     M.click(xunfei_dict_clear[0], xunfei_dict_clear[1])
#     time.sleep(1)
#     box = get_configwindow()
#     xunfei_dict_clear_enter_button = (int(box.x + box.width * PARAMS[INPUT]['pinyin_clear_enter_button'][0]),
#                                       int(box.y + box.height * PARAMS[INPUT]['pinyin_clear_enter_button'][1]))
#     M.click(xunfei_dict_clear_enter_button[0], xunfei_dict_clear_enter_button[1])
#     time.sleep(3)
#     box = get_configwindow()
#     close_config_button = (int(box.x + box.width * PARAMS[INPUT]['close_config_window'][0]),
#                            int(box.y + box.height * PARAMS[INPUT]['close_config_window'][1]))
#     M.click(close_config_button[0], close_config_button[1])
#     time.sleep(1)


# 讯飞输入法属性设置框点击会导致输入法崩溃不可用，暂时使用删除词库的方式清空词库
def xunfeipinyin_dict_clear1():
    start_edit(EDIT)
    key_input('a')
    time.sleep(0.5)
    x1, y1, x2, y2 = 0, 0, 0, 0
    for i in range(5):
        if get_box_coordinate('xunfei'):
            x1, y1, x2, y2 = get_box_coordinate('xunfei')
            break
        time.sleep(2)
    if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
        return
    get_config_button = (int((x1 + x2) / 2),
                         int((y1 + y2) / 2))
    M.click(get_config_button[0], get_config_button[1], button=2)
    time.sleep(1)
    open_config = open_xunfei_Property_setting_window()
    if open_config:
        open_config_button = (int(open_config.x + open_config.width * PARAMS[INPUT]['open_config_window'][0]),
                              int(open_config.y + open_config.height * PARAMS[INPUT]['open_config_window'][1]))
        M.click(open_config_button[0], open_config_button[1])
    time.sleep(5)
    box = get_configwindow()
    # clear pinyin dict
    xunfei_dict_button = (int(box.x + box.width * PARAMS[INPUT]['pinyin_dict_button'][0]),
                          int(box.y + box.height * PARAMS[INPUT]['pinyin_dict_button'][1]))
    M.click(xunfei_dict_button[0], xunfei_dict_button[1])
    time.sleep(1)
    xunfei_dict_clear = (int(box.x + box.width * PARAMS[INPUT]['pinyin_clear_button'][0]),
                         int(box.y + box.height * PARAMS[INPUT]['pinyin_clear_button'][1]))
    M.click(xunfei_dict_clear[0], xunfei_dict_clear[1])
    time.sleep(1)
    box = get_configwindow()
    xunfei_dict_clear_enter_button = (int(box.x + box.width * PARAMS[INPUT]['pinyin_clear_enter_button'][0]),
                                      int(box.y + box.height * PARAMS[INPUT]['pinyin_clear_enter_button'][1]))
    M.click(xunfei_dict_clear_enter_button[0], xunfei_dict_clear_enter_button[1])
    time.sleep(3)
    box = get_configwindow()
    close_config_button = (int(box.x + box.width * PARAMS[INPUT]['close_config_window'][0]),
                           int(box.y + box.height * PARAMS[INPUT]['close_config_window'][1]))
    M.click(close_config_button[0], close_config_button[1])
    time.sleep(1)
    close_edit(EDIT)
    time.sleep(10)


def xunfeipinyin_dict_clear():
    dict_name = ['userdict.bin']
    for i in range(len(dict_name)):
        clear_dict = '$HOME/.config/iflytek/' + dict_name[i]
        if os.path.exists(clear_dict):
            cmd = "rm " + clear_dict
            os.popen(cmd)
