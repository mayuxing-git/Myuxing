# 输入法切换速度：
# 系统冷启动
# 进程冷启动
# 非首次切出
from config import INPUT, EDIT
from fake_input import start_edit, close_edit
from window_impl import get_status_box_geometry
from image_manage import get_status_box_time
from keys import do, shift, ctrl
import time


class Task(object):
    def __init__(self):
        self.result_file = 'log.txt'
        self.input = INPUT
        self.edit = EDIT
        self.repeat = 50
        self.box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}

    def system_cold_start(self):
        res = {'min': 10000, 'max': 0, 'avg': 0}
        time_list = []
        start_edit(self.edit)
        item = get_status_box_time(self.box)
        time_list.append(item)
        close_edit(self.edit)
        time.sleep(1)
        res['avg'] = time_list[0]
        res['min'] = res['avg']
        res['max'] = res['avg']
        return res

    def proc_cold_start(self):
        res = {'min': 10000, 'max': 0, 'avg': 0}
        time_list = []
        for i in range(self.repeat):
            start_edit(self.edit)
            item = get_status_box_time(self.box)
            time_list.append(item)
            close_edit(self.edit)
            time.sleep(1)
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

    def proc_hot_start(self):
        res = {'min': 10000, 'max': 0, 'avg': 0}
        time_list = []
        start_edit(self.edit)
        do(ctrl + shift)
        time.sleep(1)
        do(ctrl + shift)
        time.sleep(1)
        for i in range(self.repeat):
            item = get_status_box_time(self.box)
            time_list.append(item)
        close_edit(self.edit)
        time.sleep(1)
        sum = 0
        count = len(time_list)
        for i in range(len(time_list)):
            if time_list[i] < 0:
                count = count -1
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
        geom = None
        if self.input == 'sogou':
            geom = get_status_box_geometry('Sogou')
        if self.input == 'xunfei':
            geom = get_status_box_geometry('xunfei')
        self.box['top'] = geom.y
        self.box['left'] = geom.x
        self.box['width'] = geom.width
        self.box['height'] = geom.height
        # 系统冷启动
        res_sys_cold = self.system_cold_start()
        # 进程冷启动
        res_proc_cold = self.proc_cold_start()
        # 非首次切出
        res_proc_hot = self.proc_hot_start()
        with open(self.result_file, 'w+') as f:
            f.write(self.input + '\n')
            f.write('system_cold_start: MIN: ' + str(res_sys_cold['min']) + '\tMAX: ' + str(res_sys_cold['max']) + '\tAVG: ' +
                    str(res_sys_cold['avg']) + '\n')
            f.write('proc_cold_start: MIN: ' + str(res_proc_cold['min']) + '\tMAX: ' + str(res_proc_cold['max']) + '\tAVG: ' +
                    str(res_proc_cold['avg']) + '\n')
            f.write('proc_hot_start: MIN: ' + str(res_proc_hot['min']) + '\tMAX: ' + str(res_proc_hot['max']) + '\tAVG: ' +
                    str(res_proc_hot['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()

