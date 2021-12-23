import subprocess,ast,time,pynput,threading,psutil
from Util.handle_txt import Handle_txt
from Util.handle_log import run_log as logger
from Util.handle_keyboard import Keyboard
from Util.To_prepar import to_prepar
from Util.Data_language import test_data, keyboard

class base_main():
    def __init__(self):
        self.ctr = pynput.keyboard.Controller()
        self.data = ''
        self.layouts = ''
        self.way = ''

    def run_mian(self):
        subprocess.Popen('ceshi.txt',shell=True)
        time.sleep(2)
        Handle_txt().clear_data()
        Handle_txt().save_data()

        test_data_reslut = list(test_data())   # test_data_reslut：0.title   1.数据    2.布局    3.上屏方式  4.标识

        self.data  = test_data_reslut[1]
        self.layouts = test_data_reslut[2]
        self.way = test_data_reslut[3]
        label = test_data_reslut[4]
        to_prepar(test_data_reslut[0])
        logger.info('当前测试数据为{}'.format(test_data_reslut[0]))
        key_list = keyboard(self.layouts, self.data)

        Keyboard().key_mapping(self.layouts, key_list, self.way,label)
#开启
#base_main().run_mian()


    def fun2(self):
        while True:
            time.sleep(2)
            p_name = 'SogouComServer.exe'
            p_list = psutil.pids()

            for i in p_list:
                if psutil.Process(i).name() == p_name:
                    # print('【{}】当前进程使用cpu：'.format(p_name), psutil.Process(i).cpu_percent())
                    # print('【{}】当前进程使用内存：'.format(p_name), psutil.Process(i).memory_info().rss)
                    # print('【{}】当前进程使用内存占比：'.format(p_name), psutil.Process(i).memory_percent())
                    # print('【{}】当前进程读取IO及字节数：'.format(p_name), psutil.Process(i).io_counters())
                    dict = {}
                    dict['cpu_usage'] = psutil.Process(i).cpu_percent()
                    dict['memory_usage'] = psutil.Process(i).memory_info().rss
                    with open('log.txt', 'a') as f:
                        f.write(
                            str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + str(dict) + '\n')

t1 = threading.Thread(target=base_main().run_mian())
t2 = threading.Thread(target=base_main().fun2())

t1.start()
t2.start()