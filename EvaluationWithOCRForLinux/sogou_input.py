import time
import os
import re
from config import INPUT, PARAMS, M
from window_impl import get_ocr_resultlist, get_configwindow
from keys import do, Enter
from fake_input import close_edit, keyboard_layout
# from cnocr import CnOcr


# 将ocr识别结果按照候选序号放入list
def get_sogou_resultlist():
    ocr_resultlist = get_ocr_resultlist('Sogou')
    if ocr_resultlist:
        result_tobe_process = ''
        for i in range(len(ocr_resultlist)):
            result_tobe_process += ocr_resultlist[i]['text']
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
            elif result_tobe_process[i] == str(cand_count + 1) and i < (res_len-1):
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


def sogoupinyin_dict_clear():
    os.popen('/usr/bin/sogouIme-configtool')
    time.sleep(1)
    box = get_configwindow()
    # clear pinyin dict
    sogoupinyin_button = (int(box.x + box.width * PARAMS[INPUT]['pinyin_dict_button'][0]),
                          int(box.y + box.height * PARAMS[INPUT]['pinyin_dict_button'][1]))
    M.click(sogoupinyin_button[0], sogoupinyin_button[1])
    time.sleep(1)
    sogoupinyin_clear = (int(box.x + box.width * PARAMS[INPUT]['pinyin_clear_button'][0]),
                         int(box.y + box.height * PARAMS[INPUT]['pinyin_clear_button'][1]))
    M.click(sogoupinyin_clear[0], sogoupinyin_clear[1])
    time.sleep(1)
    do(Enter)
    time.sleep(1)
    do(Enter)
    time.sleep(1)
    do(Enter)
    time.sleep(1)


def sogou_virtualkeyboard_dict_clear():
    dict_name = keyboard_layout['dict_name']
    close_edit('sogouImeService')
    time.sleep(10)
    for i in range(len(dict_name)):
        clear_dict = '$HOME/.config/SogouShell/usr/PYDict/' + dict_name[i]
        if os.path.exists(clear_dict):
            cmd = "rm " + clear_dict
            os.popen(cmd)


# 将虚拟键盘OCR识别结果的保留候选文本转为list
def standardization_canlist(cand_list):
    standard_candlist = []
    for i in range(len(cand_list)):
        standard_candlist.append(cand_list[i]['text'])
    return standard_candlist


if __name__ == '__main__':
    result_tobe_process = 'f2fd3fsd'
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
    print(new_result)
