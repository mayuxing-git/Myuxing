# 键盘调起速度：语音键盘
# 系统冷启动
# 系统热启动

from config import INPUT, EDIT
from fake_input import start_edit, close_edit
from window_impl import get_voiceinput_geometry
from image_manage import get_voiceinput_box_time, get_voiceinput_window_box
from keys import do, shift, ctrl
import time


class Task(object):
    def __init__(self):
        self.result_file = 'voiceinput_start_log.txt'
        self.input = INPUT
        self.edit = EDIT
        self.repeat = 50
        self.box = {'top': 1790, 'left': 880, 'width': 125, 'height': 156}

    def system_cold_start(self):
        res = {'min': 10000, 'max': 0, 'avg': 0}
        time_list = []
        # start_edit(self.edit)
        do(ctrl + shift)
        time.sleep(1)
        if self.input == 'sogou':
            voice_window = get_voiceinput_window_box('Sogou')
        elif self.input == 'xunfei':
            voice_window = get_voiceinput_window_box('xunfei')
        self.box['top'] = voice_window.y
        self.box['left'] = voice_window.x
        self.box['width'] = voice_window.width
        self.box['height'] = voice_window.height
        if self.input == 'sogou':
            item = get_voiceinput_box_time('Sogou', self.box)
            time_list.append(item)
        elif self.input == 'xunfei':
            item = get_voiceinput_box_time('xunfei', self.box)
            time_list.append(item)
        time.sleep(2)
        do(ctrl + shift)
        # close_edit(self.edit)
        # time.sleep(1)
        if time_list[0] > 0:
            res['avg'] = time_list[0]
            res['min'] = res['avg']
            res['max'] = res['avg']
        return res

    def system_hot_start(self):
        res = {'min': 10000, 'max': 0, 'avg': 0}
        time_list = []
        # start_edit(self.edit)
        do(ctrl + shift)
        time.sleep(1)
        for i in range(self.repeat):
            if INPUT == 'sogou':
                item = get_voiceinput_box_time('Sogou', self.box)
            elif INPUT == 'xunfei':
                item = get_voiceinput_box_time('xunfei', self.box)
            time_list.append(item)
        time.sleep(1)
        # close_edit(self.edit)
        sum = 0
        count = len(time_list)
        for i in range(len(time_list)):
            if time_list[i] < 0:
                count = count - 1
                continue
            sum += time_list[i]
            if res['min'] > time_list[i]:
                res['min'] = time_list[i]
            if res['max'] < time_list[i]:
                res['max'] = time_list[i]
        if count:
            res['avg'] = int(sum / count)
        return res

    def run(self):
        # 系统冷启动
        res_sys_cold = self.system_cold_start()
        time.sleep(5)
        # if self.input == 'sogou':
        # geom = get_sogou_voiceinput_geometry()
        # self.box['top'] = geom.y
        # self.box['left'] = geom.x
        # self.box['width'] = geom.width
        # self.box['height'] = geom.height
        # time.sleep(1)

        # 系统热启动
        res_sys_hot = self.system_hot_start()
        with open(self.result_file, 'w+') as f:
            f.write(self.input + '\n')
            f.write('system_cold_start: MIN: ' + str(res_sys_cold['min']) + '\tMAX: ' + str(
                res_sys_cold['max']) + '\tAVG: ' +
                    str(res_sys_cold['avg']) + '\n')
            f.write('system_hot_start: MIN: ' + str(res_sys_hot['min']) + '\tMAX: ' + str(
                res_sys_hot['max']) + '\tAVG: ' +
                    str(res_sys_hot['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()
