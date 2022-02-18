import time
import os
import re
from config import INPUT, PARAMS, M
from window_impl import get_sogou_configwindow
from keys import do, Enter


# 清除词库
def sogoupinyin_dict_clear():
    os.popen('/usr/bin/sogouIme-configtool')
    time.sleep(1)
    box = get_sogou_configwindow()
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


def standardization_canlist(cand_list):
    standard_candlist = []
    for i in range(len(cand_list)):
        standard_candlist.append(cand_list[i]['text'])
    return standard_candlist
