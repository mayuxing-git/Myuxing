# 虚拟键盘候选上屏速度：
from config import EDIT, INPUT
from fake_input import start_edit, close_edit, virtualkey_input, virtualkey_delete_pinyin, init_virtualkey_layout, \
    virtualkey_click_first_cand
from keys import do, ctrl, shift, BackSpace
from window_impl import get_cand_virtual_keyboard_geometry, get_virtual_keyboard_geometry, get_first_on_screen_area
from image_manage import get_press_key_response_time
import os
import time
import json


class Task(object):
    def __init__(self):
        self.edit = EDIT
        self.input = INPUT
        self.result_file = 'log.txt'
        self.keyboard_type = 26
        self.repeat = 2
        self.box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}
        self.keyboard = None

    def run(self):
        time.sleep(0.5)
        start_edit(self.edit)
        time.sleep(1)
        geom = get_first_on_screen_area()
        do(ctrl + shift)
        time.sleep(3)
        init_virtualkey_layout()
        time.sleep(1)
        virtualkey_input('b', self.keyboard_type)
        time.sleep(0.5)
        self.box['top'] = geom[1]
        self.box['left'] = geom[0]
        self.box['width'] = geom[2] - geom[0]
        self.box['height'] = geom[3] - geom[1]
        self.keyboard = get_virtual_keyboard_geometry('Sogou')
        virtualkey_delete_pinyin('b', self.keyboard_type)
        time.sleep(1)
        time_list = []
        for i in range(self.repeat):
            pinyin = 'ni'
            virtualkey_input(pinyin, self.keyboard_type)
            time.sleep(0.5)
            virtualkey_click_first_cand()
            res_item = get_press_key_response_time(self.box)
            time_list.append(res_item)
            do(BackSpace)
            time.sleep(0.1)
        close_edit(self.edit)
        first_res = {'min': 10000, 'max': 0, 'avg': 0}
        sum = 0
        count = len(time_list)
        for i in range(len(time_list)):
            if time_list[i] < 0:
                count = count - 1
                continue
            sum += time_list[i]
            if first_res['min'] > time_list[i]:
                first_res['min'] = time_list[i]
            if first_res['max'] < time_list[i]:
                first_res['max'] = time_list[i]
        if count:
            first_res['avg'] = int(sum / count)
        with open(self.result_file, 'w+') as f:
            f.write(self.input + '\n')
            f.write('cand_display_on_screen_time_virtual: MIN: ' + str(first_res['min']) + '\tMAX: ' + str(first_res['max']) + '\tAVG: ' +
                    str(first_res['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()
