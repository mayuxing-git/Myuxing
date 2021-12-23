import pynput,time
class Handle_txt():
    def __init__(self):
        self.ctr = pynput.keyboard.Controller()

    def save_data(self):
        '''保存模块：正序 按下ctrl s 按键列表'''
        with self.ctr.pressed(pynput.keyboard.KeyCode.from_vk(17),
                              pynput.keyboard.KeyCode.from_vk(83)):
            pass
        # 逆序 释放按键列表
        with self.ctr.pressed(pynput.keyboard.Key.esc):
            pass

    def clear_data(self):
        '''清空模块：正序 按下ctrl a  backspace 按键列表'''
        with self.ctr.pressed(pynput.keyboard.KeyCode.from_vk(17),
                              pynput.keyboard.KeyCode.from_vk(65),
                              pynput.keyboard.KeyCode.from_vk(8)):
            pass

        time.sleep(0.5)
        # 逆序 释放按键列表
        with self.ctr.pressed(pynput.keyboard.Key.esc):
            pass
