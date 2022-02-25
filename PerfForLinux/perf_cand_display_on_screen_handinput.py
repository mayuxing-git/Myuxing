# 输入法手写键盘候选上屏速度：
from config import INPUT, EDIT, PARAMS, M
from fake_input import start_edit, close_edit, click_handinput_cand, handinput, click_xunfei_handinput_cand
from window_impl import get_status_box_geometry, get_handinput_cand_area, get_first_on_screen_area, get_handinput_window
from image_manage import get_press_key_response_time
from keys import do, shift, ctrl, BackSpace
import time

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
        self.box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}
        self.handinput_mode = 'single_word_handinput'

    def run(self):
        start_edit(self.edit)
        time.sleep(1)
        # geom = get_first_on_screen_area()
        do(ctrl + shift)
        time.sleep(1)
        if self.input == 'sogou':
            box_status = get_status_box_geometry('Sogou')
            click_button = (int(box_status.x + box_status.width * PARAMS[INPUT]['handinput_btn'][0]),
                            int(box_status.y + box_status.height * PARAMS[INPUT]['handinput_btn'][1]))
            M.click(click_button[0], click_button[1])
            time.sleep(3)
            geom = get_handinput_window()
        elif self.input == 'xunfei':
            box_status = get_status_box_geometry('xunfei')
            click_button = (int(box_status.x + box_status.width * PARAMS[INPUT]['handinput_btn'][0]),
                            int(box_status.y + box_status.height * PARAMS[INPUT]['handinput_btn'][1]))
            M.click(click_button[0], click_button[1])
            time.sleep(3)
            geom = get_handinput_window()
        self.box['top'] = geom[1]
        self.box['left'] = geom[0]
        # self.box['width'] = geom[2] - geom[0]
        # self.box['height'] = geom[3] - geom[1]
        self.box['width'] = geom[3]
        self.box['height'] = geom[2]
        time.sleep(1)
        time_list = []
        for i in range(self.repeat):
            handinput(handinput_list)
            time.sleep(1)
            if INPUT == 'sogou':
                click_handinput_cand(1)
            elif INPUT == 'xunfei':
                click_xunfei_handinput_cand(self.handinput_mode, 1)
                pass
            res_item = get_press_key_response_time(self.box)
            time_list.append(res_item)
            do(BackSpace)
            time.sleep(0.5)
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
            f.write('cand_display_on_screen_time_handinput: MIN: ' + str(time_res['min']) + '\tMAX: ' + str(time_res['max']) +
                    '\tAVG: ' + str(time_res['avg']) + '\n')


if __name__ == '__main__':
    t = Task()
    t.run()
