# 输入法手写键盘首次切出的cpu和内存占用：
from config import INPUT, EDIT, KEYBOARD_TYPE, M, PARAMS
from fake_input import start_edit, close_edit, handinput
from window_impl import get_handinput_pid, get_status_box_geometry, get_handinput_window
from keys import do, shift, ctrl, BackSpace
import time
import psutil

handinput_list = [[498, 1536], [498, 1536], [508, 1530], [560, 1511], [582, 1505], [594, 1500], [604, 1499],
                  [608, 1499], [606, 1508], [599, 1529], [594, 1535], [594, 1535], [-1, 0], [525, 1624], [525, 1624],
                  [525, 1624], [520, 1629], [518, 1630], [518, 1631], [522, 1629], [537, 1620], [580, 1603],
                  [608, 1590], [623, 1584], [628, 1582], [632, 1582], [631, 1590], [611, 1641], [580, 1689],
                  [561, 1729], [546, 1758], [537, 1775], [534, 1783], [534, 1786], [534, 1786], [-1, 0], [648, 1673],
                  [648, 1673], [647, 1681], [649, 1718], [653, 1737], [656, 1745], [663, 1750], [680, 1751],
                  [709, 1732], [739, 1706], [751, 1681], [751, 1681], [-1, 0], [-1, -1]]


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
        start_edit(self.edit)
        box_status = get_status_box_geometry('Sogou')
        click_button = (int(box_status.x + box_status.width * PARAMS[INPUT]['handinput_btn'][0]),
                        int(box_status.y + box_status.height * PARAMS[INPUT]['handinput_btn'][1]))
        repeat_time = 0
        cpu_usage = list()
        memory_usage = list()
        do(ctrl + shift)
        time.sleep(1)
        while repeat_time < self.repeat:
            M.click(click_button[0], click_button[1])
            time.sleep(3)
            handinput_pid = get_handinput_pid(PARAMS[INPUT]['handinput_service_name'])
            proc_list = []
            for i in range(len(handinput_pid)):
                try:
                    proc = psutil.Process(handinput_pid[i])
                    proc_list.append(proc)
                except psutil.NoSuchProcess:
                    pass
            # 首次调用cpu_percent()，作为计算cpu标志位
            for i in range(len(proc_list)):
                try:
                    proc_list[i].cpu_percent()
                except psutil.NoSuchProcess:
                    pass
            cpu_total_usage = 0
            memory_total_usage = 0
            handinput(handinput_list)
            for i in range(len(proc_list)):
                try:
                    cpu_total_usage += proc_list[i].cpu_percent()
                    memory_total_usage += proc_list[i].memory_full_info().uss
                except psutil.NoSuchProcess:
                    pass
            # time.sleep(3)
            # handinput(handinput_list)
            cpu_usage.append(cpu_total_usage)
            memory_usage.append(memory_total_usage)
            box_hand = get_handinput_window()
            time.sleep(1)
            click_button_close_handinput = (int(box_hand.x + box_hand.width * PARAMS[INPUT]['handinput_close'][0]),
                                            int(box_hand.y + box_hand.height * PARAMS[INPUT]['handinput_close'][1]))
            M.click(click_button_close_handinput[0], click_button_close_handinput[1])
            time.sleep(3)
            repeat_time += 1
        close_edit(self.edit)
        cpu_res = {'min': 1000, 'max': 0, 'avg': 0}
        memory_res = {'min': 100000000, 'max': 0, 'avg': 0}
        sum = 0
        count = len(cpu_usage)
        for i in range(len(cpu_usage)):
            if cpu_usage[i] < 0:
                count = count - 1
                continue
            sum += cpu_usage[i]
            if cpu_res['min'] > cpu_usage[i]:
                cpu_res['min'] = cpu_usage[i]
            if cpu_res['max'] < cpu_usage[i]:
                cpu_res['max'] = cpu_usage[i]
        if count:
            cpu_res['avg'] = int(sum / count)
        sum = 0
        count = len(memory_usage)
        for i in range(len(memory_usage)):
            if memory_usage[i] < 0:
                count = count - 1
                continue
            sum += memory_usage[i]
            if memory_res['min'] > memory_usage[i]:
                memory_res['min'] = memory_usage[i]
            if memory_res['max'] < memory_usage[i]:
                memory_res['max'] = memory_usage[i]
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
