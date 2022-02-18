import os
import requests
import json
import time
import shutil
from file import mkdir, delete_file
from fake_input import key_input, delete_pinyin, start_edit, close_edit, ctrl_shift
from sogou_input import get_sogou_resultlist, sogoupinyin_dict_clear
from config import INPUT, EDIT
from window_impl import return_default_box, get_box_coordinate, get_default_cand_box
from xunfei_input import get_xunfei_resultlist, xunfeipinyin_dict_clear
from keys import do, space, BackSpace
from ime_cpu_and_memory_usage import get_cpu_and_memory_usage, stop_thread
import threading
#from raven import Client

#DSN = 'http://8bc4d2f33f2e4c9fb6d20f86f7635414@10.162.129.144:9000/7'
#client = Client(DSN)


class Task(object):
    def __init__(self, get_task_url, upload_result_url, is_step=True):
        self.get_task_url = get_task_url
        self.upload_result_url = upload_result_url
        self.is_step = is_step
        self.id = ''
        self.all_word_num = 0
        self.finished_word_num = 0
        self.corpus_result_path = 'result.json'
        self.input = INPUT
        self.edit = EDIT
        self.log_file = 'log.txt'
        self.corpus_test = 'http://file.mt.sogou.com/g4/M00/03/A2/Co4tlV4FtxuAeTtYAAH0OREgv4g57.json?n=littlevalvalval%2540163.com_26key.json'

    def get_next(self):
        self.result_list = list()
        self.cpu_usage = dict()
        self.memory_usage = dict()
        task_info = dict()
        task_info['task_id'] = 2
        task_info['keyboard_type'] = 26
        task_info['download_url'] = self.corpus_test
        self.id = str(task_info['task_id'])
        self.work_dir = self.id
        self.keyboard_type = task_info['keyboard_type']
        corpus_download_url = task_info['download_url']

        # if os.path.exists(self.work_dir):
        #     shutil.rmtree(os.path.join(os.getcwd(), self.work_dir))
        # mkdir(self.work_dir)

        self.corpus_path = os.path.join(self.work_dir, 'corpus.json')

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
                result_json = dict()
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
            os.rename(self.corpus_result_path, str(self.id) + '.json')
            # delete_file(self.corpus_result_path)
        requests.post(url=self.upload_result_url, headers=headers, data=request_data)

    def upload_result_file(self):
        url = "http://minos.sogou/api/files"
        headers = {'Content-Type': 'multipart/form-data'}

        result_file = {
            'file': open(self.corpus_result_path, 'rb')
        }
        req = requests.post(url, headers, files=result_file)
        return json.loads(req.text)['data']

    def do_perf(self, pinyin, expect_cand):
        failure_time = 0
        mark = -1
        index = -1
        cand_list = []
        while failure_time < 3:
            mark = key_input(pinyin)
            if mark != 1:
                break
            failure_time += 1
            if self.input == 'sogou':
                cand_list = get_sogou_resultlist()
            elif self.input == 'xunfei':
                cand_list = get_xunfei_resultlist()
            if len(cand_list) == 0:
                delete_pinyin(pinyin)
                time.sleep(0.05)
                continue
            else:
                for i in range(0, len(cand_list)):
                    if cand_list[i] == expect_cand:
                        index = i + 1
                        break
                if index == -1:
                    delete_pinyin(pinyin)
                    time.sleep(0.05)
                else:
                    if self.input == 'sogou':
                        key_input(str(index))
                        time.sleep(0.01)
                        return_default_box()
                    elif self.input == 'xunfei':
                        pre_box = get_default_cand_box()
                        key_input(str(index))
                        time.sleep(0.01)
                        cur_box = get_default_cand_box()
                        if cur_box.width != pre_box.width:
                            do(space)
                            time.sleep(0.01)
                    break
        if mark == 1:
            word_info = dict()
            word_info['pinyin'] = pinyin
            word_info['cand_list'] = cand_list
            word_info['target_num'] = index
            word_info['expect_cand'] = expect_cand
            self.result_list.append(word_info)
        else:
            word_info = dict()
            word_info['pinyin'] = pinyin
            word_info['expect_cand'] = expect_cand
            self.result_list.append(word_info)

    def run(self):
        while True:
            if self.all_word_num == 0 or self.finished_word_num >= self.all_word_num:
                if self.get_task_url == '':
                    return
                try:
                    self.get_next()
                    close_edit(self.edit)
                    if self.input == 'sogou':
                        get_box_coordinate('Sogou')
                        # sogoupinyin_dict_clear()
                    elif self.input == 'xunfei':
                        start_edit(self.edit)
                        ctrl_shift()
                        time.sleep(2)
                        key_input('a')
                        time.sleep(0.5)
                        do(BackSpace)
                        time.sleep(0.5)
                        close_edit(self.edit)
                        get_box_coordinate('xunfei')
                        # xunfeipinyin_dict_clear()
                except Exception as e:
                    print(e)
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
                    get_cpu_memory_usage = threading.Thread(target=get_cpu_and_memory_usage,
                                                            args=(self.cpu_usage, self.memory_usage))
                    get_cpu_memory_usage.start()
                    for i in range(self.finished_word_num, self.all_word_num):
                        pinyin = self.word_list[i]['pinyin']
                        expect_cand = self.word_list[i]['expect_cand']
                        self.do_perf(pinyin, expect_cand)
                        self.finished_word_num = self.finished_word_num + 1
                        if self.finished_word_num > 100:
                            if len(self.cpu_usage) == 0:
                                break
                        if self.finished_word_num > 9000: #输入＞该数时退出
                            result_json = dict()
                            result_json['word_num'] = self.finished_word_num
                            result_json['word_list'] = self.result_list
                            result_json['cpu_usage'] = self.cpu_usage
                            result_json['memory_usage'] = self.memory_usage
                            json.dump(result_json, open(self.corpus_result_path, "w"))
                            break
                        if self.finished_word_num % 100000 == 0 and self.finished_word_num < self.all_word_num:
                            self.upload_result()
                    if self.finished_word_num >= self.all_word_num:
                        self.upload_result()
                        self.all_word_num = 0
                        self.finished_word_num = 0
                    stop_thread(get_cpu_memory_usage)
                    close_edit(self.edit)
                    break
                except Exception as e:
                    print(e)
                    print(self.finished_word_num)
                    stop_thread(get_cpu_memory_usage)
                    close_edit(self.edit)
                    print("run error!")


if __name__ == '__main__':
    task = Task('http://minos.qa.sogou:5000/api/task/info/pending?platform=linux',
                'http://minos.qa.sogou:5000/api/task/info/running')
    # task = Task('http://minos.qa.sogou/api/task/info/test?task_id=95977',
    #             'http://minos.qa.sogou/api/task/info/running')
    task.run()
