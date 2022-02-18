# 输入法候选上屏速度：
from config import INPUT, EDIT, KEYBOARD_TYPE
from fake_input import start_edit, close_edit, delete_pinyin
from window_impl import get_cand_box_geometry
from image_manage import get_press_key_response_time
from keys import do, shift, ctrl, BackSpace, space
import time


class Task(object):
    def __init__(self):
        self.result_file = 'log.txt'
        self.input = INPUT
        self.edit = EDIT
        self.repeat = 50
        self.keyboard_type = KEYBOARD_TYPE
        self.box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}

    def run(self):
        start_edit(self.edit)
        time.sleep(1)
        do(ctrl + shift)
        time.sleep(1)
        do('b')
        time.sleep(1)
        geom = None
        if self.input == 'sogou':
            geom = get_cand_box_geometry('Sogou')
        elif self.input == 'xunfei':
            geom = get_cand_box_geometry('xunfei')
        self.box['top'] = geom.y
        self.box['left'] = geom.x
        self.box['width'] = geom.width
        self.box['height'] = geom.height
        do(BackSpace)
        time.sleep(1)
        time_list = []
        for i in range(self.repeat):
            pinyin = 'wo'
            do(pinyin)
            res_item = get_press_key_response_time(self.box)
            time_list.append(res_item)
            delete_pinyin(pinyin)
            time.sleep(0.1)
        close_edit(self.edit)
        time_res = {'min': 10000, 'max': 0, 'avg': 0}
        sum = 0
        count = len(time_list)
        for i in range(len(time_list)):
            if time_list[i] < 0:
                count = count - 1
                continue
            sum += time_list[i]
            if time_res['min'] > time_list[i]:
                time_res['min'] = time_list[i]
            if time_res['max'] < time_list[i]:
                time_res['max'] = time_list[i]
        if count:
            time_res['avg'] = int(sum / count)
        with open(self.result_file, 'w+') as f:
            f.write(self.input + '\n')
            f.write('cand_display_on_screen_time: MIN: ' + str(time_res['min']) + '\tMAX: ' + str(time_res['max']) +
                    '\tAVG: ' + str(time_res['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()
