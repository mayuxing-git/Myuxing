import pynput,subprocess,time
from Util.handle_txt import Handle_txt
from Util.handle_log import run_log as logger

class Ruidian():
    def __init__(self):
        self.ctr = pynput.keyboard.Controller()
        self.min_data = [
            [{'á':['219','65']},{'é':['219','69']},{'í':['219','73']},{'ó':['219','79']},{'ú':['219','85']},{'ý':['219','89']},
             {'ä':['186','65']},{'ë':['186','69']},{'ï':['186','73']},{'ö':['186','79']},{'ü':['186','85']},{'ÿ':['186','89']},],
            [{'à':['219','65']},{'è':['219','69']},{'ì':['219','73']},{'ò':['219','79']},{'ù':['219','85']},
             {'â':['186','65']},{'ê':['186','69']},{'î':['186','73']},{'ô':['186','79']},{'û':['186','85']},],
            [{'ã':['186','65']},{'ñ':['186','78']},{'õ':['186','79']},]
        ]
        self.max_data = [
            [{'Á':['219','65']},{'É':['219','69']},{'Í':['219','73']},{'Ó':['219','79']},{'Ú':['219','85']},{'Ý':['219','89']},
             {'Ä':['186','65']},{'Ë':['186','69']},{'Ï':['186','73']},{'Ö':['186','79']},{'Ü':['186','85']},{'Ÿ':['186','89']},],
            [{'À':['219','65']},{'È':['219','69']},{'Ì':['219','73']},{'Ò':['219','79']},{'Ù':['219','85']},
             {'Â':['186','65']},{'Ê':['186','69']},{'Î':['186','73']},{'Ô':['186','79']},{'Û':['186','85']},],
            [{'Ã':['186','65']},{'Ñ':['186','78']},{'Õ':['186','79']},]
        ]

    def run_mian(self):
        subprocess.Popen('ceshi.txt', shell=True)
        time.sleep(2)
        Handle_txt().clear_data()
        Handle_txt().save_data()
        time.sleep(5)
        #
        self.test_min_data()
        self.test_max_data()
    def test_min_data(self):
        for data in self.min_data[0]:
            for key, value in data.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)
                result = self.txt()
                if result.split(' ')[0] == key:
                    print('成功{}{}'.format(key, result))
                    break
                else:
                    logger.error('匹配错误:预期 右alt+{}+{}->{}  上屏->{}'.format(value[0], value[1], key, result))
        for data in self.min_data[1]:
            for key,value in data.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)
                result = self.txt()
                if result.split(' ')[0] == key:
                    print('成功{}{}'.format(key, result))
                    break
                else:
                    logger.error('匹配错误:预期 右alt+{}+{}->{}  上屏->{}'.format(value[0], value[1], key, result))
        for data in self.min_data[2]:
            for key, value in data.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(18))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(18))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)
                result = self.txt()
                if result.split(' ')[0] == key:
                    print('成功{}{}'.format(key, result))
                    break
                else:
                    logger.error('匹配错误:预期 右alt+{}+{}->{}  上屏->{}'.format(value[0], value[1], key, result))
    def test_max_data(self):
        for data in self.max_data[0]:
            for key, value in data.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(20))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(20))

                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))

                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(20))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(20))
                result = self.txt()
                if result.split(' ')[0] == key:
                    print('成功{}{}'.format(key, result))
                    break
                else:
                    logger.error('匹配错误:预期 cpas+{}+{}->{}  上屏->{}'.format(value[0], value[1], key, result))


        for data in self.max_data[1]:

            for key, value in data.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(20))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(20))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))

                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))

                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(20))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(20))
                result = self.txt()
                if result.split(' ')[0] == key:
                    print('成功{}{}'.format(key, result))
                    break
                else:
                    logger.error('匹配错误:预期 cpas+shift+{}+{}->{}  上屏->{}'.format(value[0], value[1], key, result))

        for data in self.max_data[2]:
            for key, value in data.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(18))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(18))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)
                result = self.txt()
                if result.split(' ')[0] == key:
                    print('成功{}{}'.format(key, result))
                    break
                else:
                    logger.error('匹配错误:预期 右alt+{}+{}->{}  上屏->{}'.format(value[0], value[1], key, result))

    def txt(self):
        Handle_txt().save_data()
        Handle_txt().clear_data()
        with open('ceshi.txt', 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == '__main__':
    Ruidian().run_mian()