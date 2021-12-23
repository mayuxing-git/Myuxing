import pynput, time
from Util.handle_txt import Handle_txt
from Util.handle_log import run_log as logger
from Test_data.data import Testdata
class Keyboard():
    def __init__(self):
        self.ctr = pynput.keyboard.Controller()
        self.num = ''

    def key_mapping(self, layouts, key_list, way, label):

        '''以布局为基础 传递 按键参数 ，发起按键映射'''
        if label == False:
            for layout in layouts:
                print(layout)
                if layout == '基础布局':
                    # print(key_list[0])
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[0]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key,values)
                    time.sleep(1)
                elif layout == 'shift布局':
                    # print(key_list[1])
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[1]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key,values)
                    time.sleep(1)
                elif layout == 'capslock布局':
                    # print(key_list[2])
                    logger.info('布局：{0}'.format(layout))
                    # '''
                    # 先开启caps，按下每个按键保存对比，全部按键执行完毕后，释放caps
                    # '''
                    self.ctr.press(pynput.keyboard.KeyCode.from_vk(20))
                    self.ctr.release(pynput.keyboard.KeyCode.from_vk(20))
                    for keys in key_list[2]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key, values)
                    self.ctr.press(pynput.keyboard.KeyCode.from_vk(20))
                    self.ctr.release(pynput.keyboard.KeyCode.from_vk(20))
                    time.sleep(1)
                elif layout == '右alt布局':

                    # print(key_list[3])
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[3]:
                        for num in range(len(list(keys))):
                            # print(list(keys.values())[num],list(keys.keys())[num])
                            if list(keys.values())[num] == '':
                                logger.info('无需关注（保证脚本不崩溃,当前语言该排按键在该布局下没有映射关系）')
                            else:

                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(17))
                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(18))
                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(list(keys.values())[num])))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(list(keys.values())[num])))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(17))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(18))

                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                                self.get_txt(list(keys.keys())[num], list(keys.values())[num])
                    time.sleep(1)
                else:
                    logger.error('当前布局类型错误：{0}'.format(list(layout.keys())))
                    break
                time.sleep(1)
        else:
            for layout in layouts:
                print(layout)
                if layout == '基础布局':
                    # print('*********')
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[0]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key,values)
                    time.sleep(1)
                elif layout == 'shift布局':
                    # print('*********')
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[1]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key,values)
                    time.sleep(1)
                elif layout == 'm布局':
                    # print('*********')
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[2]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(77))
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(77))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key,values)
                    time.sleep(1)
                elif layout == 'ctrl+alt+shift布局':
                    # print('*********')
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[3]:
                        for key,values in keys.items():
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(17))
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(18))
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(values)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(18))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(17))

                            self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                            self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                            self.get_txt(key,values)
                    time.sleep(1)
                elif layout == 'shift+m布局':
                    # print('*********')
                    logger.info('布局：{0}'.format(layout))
                    for keys in key_list[4]:
                        for num in range(len(list(keys))):
                            # print(list(keys.values())[num],list(keys.keys())[num])
                            if list(keys.values())[num] == '':
                                logger.info('特殊按键无需关注（保证脚本不崩溃）')
                            else:

                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(77))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(77))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))

                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(list(keys.values())[num])))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(list(keys.values())[num])))

                                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(way)))
                                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(way)))

                                self.get_txt(list(keys.keys())[num], list(keys.values())[num])
                    time.sleep(1)
                else:
                    logger.error('当前布局类型错误：{0}'.format(list(layout.keys())))
                    break

    def get_txt(self,key,values):
        '''获取文件内容，进行比对校验'''
        Handle_txt().save_data()
        Handle_txt().clear_data()
        with open('ceshi.txt','r',encoding='utf-8') as f:
            data = f.read()
            default = Testdata().default_data()
            if key == data.split(' ')[0]:
                i = [i for i, j in default.items() if values == j]
                print('键盘：{0} 键映射正常：预期结果：{1} -> 实际结果{2}'.format(i,key,data))
                # logger.info('键盘：{0} 键映射正常：预期结果：{1} -> 实际结果{2}'.format(i,key,data))

            else:
                i= [i for i, j in default.items() if values == j]
                logger.error('键盘{0} 键映射异常：预期结果{1} -> 实际结果{2}'.format(i, key, data))

