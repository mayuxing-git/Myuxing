# 虚拟键盘按键响应速度
from config import EDIT, INPUT
from fake_input import start_edit, close_edit, delete_pinyin, virtualkey_input, virtualkey_delete_pinyin, \
    virtualkey_click_event, init_virtualkey_layout
from keys import do, ctrl, shift
from window_impl import get_cand_virtual_keyboard_geometry, get_virtual_keyboard_geometry
from image_manage import get_press_key_response_time
import os
import time
import json


class Task(object):
    def __init__(self):
        self.edit = EDIT
        self.input = INPUT
        self.result_file = 'log.txt'
        self.corpus_file = 'corpus_26key.json'
        self.keyboard_type = 26
        self.word_list = []
        self.box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}
        self.keyboard = None

    def run(self):
        if not os.path.exists(self.corpus_file):
            with open(self.result_file, 'w+') as f:
                f.write('Not found corpus file' + self.corpus_file)
            print('Not found corpus file!!!')
        data = json.load(open(self.corpus_file))
        self.word_list = data['word_list']
        time.sleep(0.5)
        start_edit(self.edit)
        time.sleep(1)
        do(ctrl + shift)
        time.sleep(1)
        init_virtualkey_layout()
        time.sleep(1)
        virtualkey_input('b', self.keyboard_type)
        time.sleep(0.5)
        if self.input == 'sogou':
            geom = get_cand_virtual_keyboard_geometry('Sogou')
            self.box['top'] = geom.y
            self.box['left'] = geom.x
            self.box['width'] = geom.width
            self.box['height'] = geom.height
            self.keyboard = get_virtual_keyboard_geometry('Sogou')
        virtualkey_delete_pinyin('b', self.keyboard_type)
        time.sleep(1)
        fist_time_list = []
        second_time_list = []
        for i in range(len(self.word_list)):
            pinyin = self.word_list[i]['pinyin']
            for p in range(len(pinyin)):
                virtualkey_click_event(pinyin[p], self.keyboard)
                res_item = get_press_key_response_time(self.box)
                if p == 0:
                    fist_time_list.append(res_item)
                else:
                    second_time_list.append(res_item)
            virtualkey_delete_pinyin(pinyin, self.keyboard_type)
            time.sleep(0.1)
        close_edit(self.edit)
        first_res = {'min': 10000, 'max': 0, 'avg': 0}
        second_res = {'min': 10000, 'max': 0, 'avg': 0}
        sum = 0
        count = len(fist_time_list)
        for i in range(len(fist_time_list)):
            if fist_time_list[i] < 0:
                count = count - 1
                continue
            sum += fist_time_list[i]
            if first_res['min'] > fist_time_list[i]:
                first_res['min'] = fist_time_list[i]
            if first_res['max'] < fist_time_list[i]:
                first_res['max'] = fist_time_list[i]
        if count:
            first_res['avg'] = int(sum / count)
        sum = 0
        count = len(second_time_list)
        for i in range(len(second_time_list)):
            if second_time_list[i] < 0:
                count = count - 1
                continue
            sum += second_time_list[i]
            if second_res['min'] > second_time_list[i]:
                second_res['min'] = second_time_list[i]
            if second_res['max'] < second_time_list[i]:
                second_res['max'] = second_time_list[i]
        if count:
            second_res['avg'] = int(sum / count)
        with open(self.result_file, 'w+') as f:
            f.write(self.input + '\n')
            f.write('first: press_key: MIN: ' + str(first_res['min']) + '\tMAX: ' + str(first_res['max']) + '\tAVG: ' +
                    str(first_res['avg']) + '\n')
            f.write('second: press_key: MIN: ' + str(second_res['min']) + '\tMAX: ' + str(second_res['max']) + '\tAVG: ' +
                    str(second_res['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()
