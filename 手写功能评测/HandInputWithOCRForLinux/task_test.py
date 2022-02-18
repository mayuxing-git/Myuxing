import os
import requests
import json
import time
from file import mkdir, delete_file
from fake_input import start_edit, close_edit, ctrl_shift, handinput, click_handinput_cand, switch_handinput_keyboard, \
    close_handinput_keyboard, click_xunfei_handinput_cand
from sogou_input import standardization_canlist, sogoupinyin_dict_clear
from config import INPUT, EDIT, PARAMS
from window_impl import get_ocr_resultlist, get_handinput_window
import threading
from ime_cpu_and_memory_usage import get_cpu_and_memory_usage, stop_thread
from performance_test_util import Get_Handinput_Response_Time
import collections


class Task(object):
    def __init__(self, get_task_url, upload_result_url, is_step=True):
        self.get_task_url = get_task_url
        self.upload_result_url = upload_result_url
        self.is_step = is_step
        self.id = ''
        self.all_word_num = 0
        self.finished_word_num = 0
        self.corpus_result_path = 'test.json'
        self.input = INPUT
        self.edit = EDIT
        self.log_file = 'log.txt'
        self.isneed_response_time = PARAMS[INPUT]['isneed_response_time']
        self.handinput_mode = 'single_word_handinput'
        # self.corpus_test = 'http://file.mt.sogou.com/g4/M00/03/A2/Co4tlV4FtxuAeTtYAAH0OREgv4g57.json?n=littlevalvalval%2540163.com_26key.json'

    # 从task中获取键盘类型handinput，并获取手写模式single_word_handinput或multi_word_handinput
    def get_next(self):
        self.result_list = list()
        self.cpu_usage = list()
        self.memory_usage = list()
        self.get_first_screen_time = list()
        self.get_first_cand_time = list()
        task_info = dict()
        task_info['task_id'] = 2
        # task_info['keyboard_type'] = 26
        # task_info['download_url'] = self.corpus_test
        self.id = str(task_info['task_id'])
        self.work_dir = self.id
        # self.keyboard_type = task_info['keyboard_type']
        # corpus_download_url = task_info['download_url']

        # if os.path.exists(self.work_dir):
        #     shutil.rmtree(os.path.join(os.getcwd(), self.work_dir))
        # mkdir(self.work_dir)

        self.corpus_path = os.path.join(self.work_dir, 'test.json')

        # with open(self.corpus_path, "wb") as corpus_file:
        #     corpus_req = requests.get(corpus_download_url)
        #     corpus_file.write(corpus_req.content)

        corpus_json = json.load(open(self.corpus_path))
        self.word_list = corpus_json['word_list']
        self.all_word_num = len(corpus_json['word_list'])
        self.finished_word_num = 0

    def upload_result(self):
        upload_info = dict()
        if self.finished_word_num < self.all_word_num:
            upload_info['task_id'] = self.id
            upload_info['execution_ratio'] = str(float(self.finished_word_num) / float(self.all_word_num))
        else:
            if not os.path.exists(self.corpus_result_path):
                result_json = collections.OrderedDict()
                result_json['word_num'] = self.finished_word_num
                result_json['word_list'] = self.result_list
                result_json['cpu_usage'] = self.cpu_usage
                result_json['memory_usage'] = self.memory_usage
                json.dump(result_json, open(self.corpus_result_path, "w"))
            upload_info['task_id'] = self.id
            upload_info['execution_ratio'] = '1'
            upload_info['status'] = 'finished'
            upload_info['result_download_url'] = self.upload_result_file()
            with open(self.log_file, 'a+') as f:
                f.write(self.id + "\t" + upload_info['result_download_url'] + "\n")
            # try:
            #     shutil.rmtree(os.path.join(os.getcwd(), self.work_dir))
            # except:
            #     print("rmtree failed: " + self.work_dir)

        if self.upload_result_url == '':
            return
        headers = {'Content-Type': 'application/json'}
        request_data = json.dumps(upload_info)
        print(upload_info)

        if os.path.exists(self.corpus_result_path):
            # os.rename(self.corpus_result_path, str(self.id) + '.json')
            delete_file(self.corpus_result_path)
        requests.post(url=self.upload_result_url, headers=headers, data=request_data)

    def upload_result_file(self):
        url = "http://minos.sogou/api/files"
        headers = {'Content-Type': 'multipart/form-data'}

        result_file = {
            'file': open(self.corpus_result_path, 'rb')
        }
        req = requests.post(url, headers, files=result_file)
        return json.loads(req.text)['data']

    def do_perf(self, input_list, except_cand):
        cand_time = 0
        if self.isneed_response_time:
            start_input_time = time.time()
            get_response_time = Get_Handinput_Response_Time(start_input_time, self.handinput_mode)
            get_response_time.start()
            mark = handinput(input_list, self.handinput_mode)
            # end_input_time = time.time()
            get_response_time.join()
            # handinput_time = end_input_time - start_input_time
            cand_time, hash_value = get_response_time.get_result()
            self.get_first_screen_time.append(cand_time)
            self.get_first_cand_time.append(cand_time)
            time.sleep(1.5)
        else:
            mark = handinput(input_list, self.handinput_mode)
            time.sleep(1.5)
        if mark:
            cand_list = get_ocr_resultlist(self.handinput_mode)
            index = -1
            if INPUT == 'sogou':
                for i in range(0, len(cand_list)):
                    if cand_list[i]['text'] == except_cand:
                        index = i + 1
                        break
                    # if index != -1:
                    #     click_handinput_cand(index)
                    #     time.sleep(0.1)
                    # else:
                    #     click_handinput_cand(1)
                    #     time.sleep(0.1)
            elif INPUT == 'xunfei':
                cand = standardization_canlist(cand_list)
                pos = cand[0].find(except_cand)
                if pos == 0:
                    index = 1
                elif pos == -1:
                    index = -1
                else:
                    index = 2
                click_xunfei_handinput_cand(self.handinput_mode, index)
            word_info = collections.OrderedDict()
            # word_info['input_list'] = input_list
            word_info['cand_list'] = standardization_canlist(cand_list)
            word_info['target_num'] = index
            word_info['except_cand'] = except_cand
            if self.isneed_response_time:
                word_info['get_first_screen_time'] = cand_time
                word_info['get_first_cand_time'] = cand_time
            self.result_list.append(word_info)
        else:
            word_info = dict()
            # word_info['input_list'] = input_list
            word_info['except_cand'] = except_cand
            self.result_list.append(word_info)

    def run(self):
        while True:
            if self.all_word_num == 0 or self.finished_word_num >= self.all_word_num:
                if self.get_task_url == '':
                    return
                try:
                    self.get_next()
                    close_edit(self.edit)
                    # if self.input == 'sogou':
                    #     sogoupinyin_dict_clear()
                except:
                    self.all_word_num = 0
                    self.finished_word_num = 0
                    print("get_next error!")
                time.sleep(1)
            else:
                try:
                    # start_edit(self.edit)  # ubuntu
                    start_edit(self.edit)  # kylin
                    time.sleep(1)
                    ctrl_shift()
                    switch_handinput_keyboard(self.handinput_mode)
                    get_handinput_window()
                    get_cpuusage = threading.Thread(target=get_cpu_and_memory_usage,
                                                    args=(self.cpu_usage, self.memory_usage))
                    get_cpuusage.start()
                    for i in range(self.finished_word_num, self.all_word_num):
                        input_list = self.word_list[i]['input_list']
                        expect_cand = self.word_list[i]['expect_cand']
                        self.do_perf(input_list, expect_cand)
                        if i % 5 == 0 and i != 0:          #5个字上屏
                            click_handinput_cand(1)
                        self.finished_word_num = self.finished_word_num + 1
                        if self.finished_word_num > 10 and len(self.cpu_usage) == 0:
                            break
                        if self.finished_word_num > 500:
                            result_json = collections.OrderedDict()
                            result_json['word_ num'] = self.finished_word_num
                            result_json['word_list'] = self.result_list
                            result_json['cpu_usage'] = self.cpu_usage
                            result_json['memory_usage'] = self.memory_usage
                            json.dump(result_json, open(self.corpus_result_path, "w"))
                            break
                        if self.finished_word_num % 1000 == 0 and self.finished_word_num < self.all_word_num:
                            self.upload_result()
                    if self.finished_word_num >= self.all_word_num:
                        self.upload_result()
                        self.all_word_num = 0
                        self.finished_word_num = 0
                    stop_thread(get_cpuusage)
                    close_handinput_keyboard()
                    close_edit(self.edit)
                    break
                except Exception as e:
                    print(e)
                    print(self.finished_word_num)
                    stop_thread(get_cpuusage)
                    break
                    close_edit(self.edit)
                    print("run error!")


if __name__ == '__main__':
    task = Task('http://minos.qa.sogou:5000/api/task/info/pending?platform=linux',
                'http://minos.qa.sogou:5000/api/task/info/running')
    # task = Task('http://minos.qa.sogou/api/task/info/test?task_id=95977',
    #             'http://minos.qa.sogou/api/task/info/running')
    task.run()
