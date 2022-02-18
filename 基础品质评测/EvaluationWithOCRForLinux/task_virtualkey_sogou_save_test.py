import os
import requests
import json
import time
import shutil
from file import mkdir, delete_file
from fake_input import key_input, delete_pinyin, start_edit, close_edit, ctrl_shift, virtualkey_input, \
    virtualkey_click_cand, init_virtualkey_layout, virtualkey_switch_keyboardtype
from sogou_input import sogou_virtualkeyboard_dict_clear, standardization_canlist
from config import EDIT, INPUT
from window_impl import return_default_box, get_box_coordinate, get_default_cand_box, get_virtualkeyboard_ocr_resultlist
from ime_cpu_and_memory_usage import get_cpu_and_memory_usage, stop_thread
import threading
from xunfei_input import get_xunfei_resultlist, xunfeipinyin_dict_clear
from keys import do, space, BackSpace
import sys
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
        self.log_file = 'log.txt'
        self.error_file = 'error.txt'
        self.corpus_result_path = 'result.json'
        self.edit = EDIT
        self.input = INPUT
        self.temp_result = 'temp_result.json'
        self.fail_count = 0
        self.keyboard_type = 26

    def manage_temp(self):
        if os.path.exists(self.temp_result):
            temp_json = json.load(open(self.temp_result))
            self.id = str(temp_json['id'])
            self.work_dir = self.id
            if not os.path.exists(self.work_dir):
                return False

            self.keyboard_type = temp_json['keyboard_type']
            self.result_list = temp_json['word_list']
            self.finished_word_num = len(self.result_list)
            if 'cpu_usage' in temp_json:
                self.cpu_usage = temp_json['cpu_usage']
            else:
                self.cpu_usage = list()
            if 'memory_usage' in temp_json:
                self.memory_usage = temp_json['memory_usage']
            else:
                self.memory_usage = list()

            self.corpus_path = os.path.join(self.work_dir, 'corpus.json')
            corpus_json = json.load(open(self.corpus_path))
            self.word_list = corpus_json['word_list']
            self.all_word_num = len(corpus_json['word_list'])

            return True
        return False

    def save_temp_result(self):
        temp_result_json = dict()
        temp_result_json['word_num'] = self.finished_word_num
        temp_result_json['word_list'] = self.result_list
        temp_result_json['id'] = self.id
        temp_result_json['keyboard_type'] = self.keyboard_type
        temp_result_json['cpu_usage'] = self.cpu_usage
        temp_result_json['memory_usage'] = self.memory_usage
        json.dump(temp_result_json, open(self.temp_result, "w"))

    def get_next(self):
        if os.path.exists(self.corpus_result_path) and self.id:
            self.all_word_num = 0
            self.finished_word_num = 0
            self.upload_result()
            return
        self.result_list = list()
        self.cpu_usage = dict()
        self.memory_usage = dict()
        task_info = dict()
        task_info['task_id'] = 2
        task_info['keyboard_type'] = 26
        # task_info['download_url'] = self.corpus_test
        # task_req = requests.get(self.get_task_url)
        # task_list = json.loads(task_req.text)['task_info']
        # if len(task_list) == 0:
        #     self.all_word_num = 0
        #     self.finished_word_num = 0
        #     time.sleep(60)
        #     return
        # task_info = task_list[0]

        self.id = str(task_info['task_id'])
        self.work_dir = self.id
        # self.keyboard_type = task_info['corpus_info']['keyboard_type']
        # corpus_download_url = task_info['corpus_info']['download_url']

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
            try:
                shutil.rmtree(os.path.join(os.getcwd(), self.work_dir))
            except:
                print("rmtree failed: " + self.work_dir)
            if os.path.exists(self.temp_result):
                delete_file(self.temp_result)

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
        url = "http://minos.qa.sogou.com/api/files"
        headers = {'Content-Type': 'multipart/form-data'}

        result_file = {
            'file': open(self.corpus_result_path, 'rb')
        }
        req = requests.post(url, headers, files=result_file)
        return json.loads(req.text)['data']

    def do_perf(self, pinyin, expect_cand):
        failure_time = 0
        while failure_time < 3:
            mark = virtualkey_input(pinyin, self.keyboard_type)
            time.sleep(0.1)
            if mark == 1:
                cand_list = get_virtualkeyboard_ocr_resultlist('Sogou')
                index = -1
                for i in range(0, len(cand_list)):
                    if cand_list[i]['text'].startswith(expect_cand):
                        index = i + 1
                        break
                # word_info = dict()
                # word_info['pinyin'] = pinyin
                # word_info['cand_list'] = standardization_canlist(cand_list)
                # word_info['target_num'] = index
                # word_info['expect_cand'] = expect_cand
                # self.result_list.append(word_info)
                if index == -1:
                    # 异常处理逻辑,未找到候选重复当前输入
                    ctrl_shift()
                    ctrl_shift()
                    failure_time += 1
                    if failure_time == 3:
                        word_info = dict()
                        word_info['pinyin'] = pinyin
                        word_info['cand_list'] = standardization_canlist(cand_list)
                        word_info['target_num'] = index
                        word_info['expect_cand'] = expect_cand
                        self.result_list.append(word_info)
                        self.fail_count += 1
                else:
                    word_info = dict()
                    word_info['pinyin'] = pinyin
                    word_info['cand_list'] = standardization_canlist(cand_list)
                    word_info['target_num'] = index
                    word_info['expect_cand'] = expect_cand
                    self.result_list.append(word_info)
                    self.fail_count = 0
                    # 点击虚拟键盘候选
                    virtualkey_click_cand(cand_list, index)
                    break
            elif mark == 2:  # 联想
                cand_list = get_virtualkeyboard_ocr_resultlist('Sogou')
                index = -1
                for i in range(0, len(cand_list)):
                    if cand_list[i]['text'].startswith(expect_cand):
                        index = i + 1
                        break
                word_info = dict()
                word_info['pinyin'] = pinyin
                word_info['cand_list'] = standardization_canlist(cand_list)
                word_info['target_num'] = index
                word_info['expect_cand'] = expect_cand
                self.result_list.append(word_info)
                if index != -1:
                    virtualkey_click_cand(cand_list, index)
                break
            else:
                word_info = dict()
                word_info['pinyin'] = pinyin
                word_info['expect_cand'] = expect_cand
                self.result_list.append(word_info)
                break

    def run(self):
        while True:
            if self.all_word_num == 0 or self.finished_word_num >= self.all_word_num:
                if self.get_task_url == '':
                    return
                try:
                    close_edit(self.edit)
                    # is_temp = self.manage_temp()
                    init_virtualkey_layout()
                    is_temp = False
                    if not is_temp:
                        if self.input == 'sogou':
                            sogou_virtualkeyboard_dict_clear()
                        self.get_next()
                except Exception as e:
                    print(e)
                    self.all_word_num = 0
                    self.finished_word_num = 0
                    print("get_next error!")
                if self.all_word_num == 0:
                    time.sleep(60)
            else:
                try:
                    if self.fail_count > 3:
                        # self.save_temp_result()
                        # self.fail_count = 0
                        sys.exit()
                    time.sleep(1)
                    start_edit(self.edit)
                    ctrl_shift()
                    virtualkey_switch_keyboardtype(self.keyboard_type)
                    begin_num = self.finished_word_num
                    get_cpu_memory_usage = threading.Thread(target=get_cpu_and_memory_usage,
                                                            args=(self.cpu_usage, self.memory_usage))
                    get_cpu_memory_usage.start()
                    for i in range(begin_num, self.all_word_num):
                        pinyin = self.word_list[i]['pinyin']
                        expect_cand = self.word_list[i]['expect_cand']
                        self.do_perf(pinyin, expect_cand)
                        print(self.fail_count)
                        self.finished_word_num = self.finished_word_num + 1
                        if self.finished_word_num % 1000 == 0 and self.finished_word_num < self.all_word_num:
                            self.upload_result()
                        if self.fail_count > 3:
                            self.save_temp_result()
                            # self.fail_count = 0
                            break
                    if self.finished_word_num >= self.all_word_num:
                        self.upload_result()
                        self.all_word_num = 0
                        self.finished_word_num = 0
                    stop_thread(get_cpu_memory_usage)
                    close_edit(self.edit)
                except Exception as e:
                    with open(self.error_file, 'a+') as f:
                        f.write(str(e) + "\n")
                    print(self.finished_word_num)
                    stop_thread(get_cpu_memory_usage)
                    close_edit(self.edit)
                    print("run error!")
                    self.fail_count += 1


if __name__ == '__main__':
    # task = Task('http://minos.qa.sogou.com/api/task/info/pending?platform=windows',
    #             'http://minos.qa.sogou.com/api/task/info/running')
    task = Task('http://minos.qa.sogou.com/api/task/info/test?task_id=367022',
                'http://minos.qa.sogou.com/api/task/info/running')
    try:
        task.run()
    except:
        task.save_temp_result()
