# 输入法首次切出的cpu和内存占用：
from config import INPUT, EDIT, KEYBOARD_TYPE
from fake_input import start_edit, close_edit
from window_impl import get_ime_pid
from keys import do, shift, ctrl, BackSpace
import time
import psutil


class Task(object):
    def __init__(self):
        self.result_file = 'log.txt'
        self.input = INPUT
        self.edit = EDIT
        self.repeat = 50
        self.keyboard_type = KEYBOARD_TYPE
        self.box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}
        self.ime_pid = None

    def run(self):
        memory_after_switch = []
        cpu_after_switch = []
        for i in range(self.repeat):
            time.sleep(0.2)
            proc_list = []
            # if i == 0:
            start_edit(EDIT)
            do(ctrl + shift)
            self.ime_pid = get_ime_pid(self.input)
            for j in range(len(self.ime_pid)):
                proc = psutil.Process(self.ime_pid[j])
                proc.cpu_percent()
                proc_list.append(proc)
            do('wo')
            memory_total_usage = 0
            cpu_total_uage = 0
            for j in range(len(proc_list)):
                memory_total_usage += proc_list[j].memory_full_info().uss
                cpu_total_uage += proc_list[j].cpu_percent()
            memory_after_switch.append(memory_total_usage)
            cpu_after_switch.append(cpu_total_uage)
            time.sleep(0.5)
            close_edit(self.edit)
            time.sleep(1)
        cpu_res = {'min': 1000, 'max': 0, 'avg': 0}
        memory_res = {'min': 100000000, 'max': 0, 'avg': 0}
        sum = 0
        count = len(cpu_after_switch)
        for i in range(len(cpu_after_switch)):
            if cpu_after_switch[i] < 0:
                count = count - 1
                continue
            sum += cpu_after_switch[i]
            if cpu_res['min'] > cpu_after_switch[i]:
                cpu_res['min'] = cpu_after_switch[i]
            if cpu_res['max'] < cpu_after_switch[i]:
                cpu_res['max'] = cpu_after_switch[i]
        if count:
            cpu_res['avg'] = int(sum / count)
        sum = 0
        count = len(memory_after_switch)
        for i in range(len(memory_after_switch)):
            if memory_after_switch[i] < 0:
                count = count - 1
                continue
            sum += memory_after_switch[i]
            if memory_res['min'] > memory_after_switch[i]:
                memory_res['min'] = memory_after_switch[i]
            if memory_res['max'] < memory_after_switch[i]:
                memory_res['max'] = memory_after_switch[i]
        if count:
            memory_res['avg'] = int(sum / count)
        with open(self.result_file, 'w+') as f:
            f.write(self.input + '\n')
            f.write('cand_display_on_screen_time: MIN: ' + str(cpu_res['min']) + '\tMAX: ' + str(cpu_res['max']) +
                    '\tAVG: ' + str(cpu_res['avg']) + '\n')
            f.write('cand_display_on_screen_time: MIN: ' + str(memory_res['min']) + '\tMAX: ' + str(memory_res['max']) +
                    '\tAVG: ' + str(memory_res['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()
