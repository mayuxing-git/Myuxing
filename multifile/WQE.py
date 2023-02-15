# coding:utf-8
# 更新时间2022/11/18 16:51
import tkinter.messagebox, xlwt, os, requests, json
from tkinter import *
from log import run_log as logger

class Application(Frame):
    def __init__(self, master=None):  # super()代表的是父类的定义，而不是父类对象
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()
        self.log = ''
        self.path = 'D:/'
        self.url = 'https://qe.wps.kingsoft.net/wqe-schedule/schedule/job/listForPage'
        self.token = ''
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'fantasy-token': ''
        }
        self.payload = {
            "current": 1,
            "size": 50,
            "startTime": "",
            "endTime": "",
            "createUser": "",
            "jobId": None,
            "fireId": "",
            "crontabId": None,
            "taskName": "",
            "priority": None,
            "jobStatus": None,
            "testProduct": None,
            "machineId": None
        }

        self.A1 = []
        self.A2 = []
        self.A3 = []
        self.A4 = []
        self.A5 = []
        self.A6 = []
        self.A7 = []
        self.A8 = []
        self.A9 = []
        self.A10 = []

    def createWidget(self):
        '''创建TK-GUI'''
        # 创建登录界面的组件
        self.label01 = Label(self, text="TOKEN")
        self.label01.pack()

        # StringVar 变量绑定到指定的组件。
        # StringVar 变量的值发生变化，组件内容也变化；
        # 组件内容发生变化，StringVar 变量的值也发生变化。 v1 = StringVar()
        v1 = StringVar()
        self.entry01 = Entry(self, textvariable=v1)
        self.entry01.pack()
        # 创建基线计划框
        self.label02 = Label(self, text="测试计划ID")
        self.label02.pack()
        v2 = StringVar()
        self.entry02 = Entry(self, textvariable=v2)
        self.entry02.pack()

        # 创建测试计划框
        self.label03 = Label(self, text="基线计划ID")
        self.label03.pack()
        v3 = StringVar()
        self.entry03 = Entry(self, textvariable=v3)
        self.entry03.pack()
        Button(self, text="开始查询", command=self.main).pack()

    def get_task_id(self,firedId):
        '''根据计划作业ID获取任务信息'''
        token = ''
        self.payload['fireId'] = firedId
        l_response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.payload))
        task_info = l_response.json()
        try:
            if task_info['code'] == 20000:
                logger.info('get_task_id - {}数据正常：{}'.format(firedId,task_info))
                job_info = task_info["data"]["records"]
                for i in job_info:
                    self.A1.append(i["jobId"])
                    self.A2.append(i["taskName"])
                    # 查linux任务分片任务信息
                    n = 0
                    for z_l_job in i['subJobInfoVoList']:
                        if z_l_job['statusName'] == '作业完成':
                            n += 1
                    self.A3.append(str(n) + '/' + str(len(i['subJobInfoVoList'])))
            else:
                logger.error('get_task_id - {}数据异常：{}'.format(firedId,task_info['msg']))
                print(task_info["msg"])
        except Exception as e:
            logger.error('get_task_id - 未知错误：{}'.format(e))
            print("getid", e)

    def get_after_job_info(self):
        '''根据前置任务ID获取后置任务名称及其ID'''
        for linux_id in self.A1:
            self.payload['fireId'] = ''
            self.payload['taskName'] = linux_id
            l_response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.payload))
            task_info = l_response.json()
            try:
                if task_info['code'] == 20000:
                    logger.info('get_after_job_info - {}数据正常:{}'.format(linux_id,task_info))
                    job_info = task_info["data"]["records"]
                    # print(len(job_info))
                    if job_info == []:
                        self.A4.append('无数据')
                        self.A5.append('无数据')
                        self.A6.append('无数据')
                    elif len(job_info) ==1:
                        for i in job_info:
                            self.A4.append(i["jobId"])
                            self.A5.append(i["taskName"])
                            # 查后置任务分片任务信息
                            n = 0
                            for j in i['subJobInfoVoList']:
                                if j['statusName'] == '作业完成':
                                    n += 1
                            self.A6.append(str(n) + '/' + str(len(i['subJobInfoVoList'])))
                    elif len(job_info) == 2:
                        w_id = []
                        w_neme = []
                        w_status = []
                        for i in job_info:
                            w_id.append(i["jobId"])
                            w_neme.append(i["taskName"])
                            # 查后置任务分片任务信息
                            n = 0
                            for j in i['subJobInfoVoList']:
                                if j['statusName'] == '作业完成':
                                    n += 1
                            w_status.append(str(n) + '/' + str(len(i['subJobInfoVoList'])))
                        self.A4.append(w_id)
                        self.A5.append(w_neme)
                        self.A6.append(w_status)

                else:
                    logger.error('get_after_job_info - {}数据异常：{}'.format(linux_id,task_info['msg']))
                    print(task_info["msg"])
            except Exception as e:
                logger.error('get_after_job_info - 未知错误：{}'.format(linux_id, task_info['msg']))
                print('gedit ', e)

    def get_compare_task(self):
        '''根据后置任务ID查找对比任务'''
        try:
            for w_id in self.A4:
                if w_id == '无数据':
                    self.A7.append('无数据')
                    self.A8.append('无数据')
                    self.A9.append('无数据')
                elif type(w_id) == str:
                    self.payload['fireId'] = ''
                    self.payload['taskName'] = w_id
                    l_response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.payload))
                    task_info = l_response.json()
                    if task_info['code'] == 20000:
                        logger.info('get_compare_task - {}数据正常：{}'.format(w_id,task_info))
                        job_info = task_info["data"]["records"]
                        if job_info == []:
                            self.A7.append('无数据')
                            self.A8.append('无数据')
                            self.A9.append('无数据')
                        elif len(job_info) == 1:
                            for i in job_info:
                                self.A7.append(i["jobId"])
                                self.A8.append(i["taskName"])
                                # 查后置任务分片任务信息
                                n = 0
                                for j in i['subJobInfoVoList']:
                                    if j['statusName'] == '作业完成':
                                        n += 1
                                self.A9.append(str(n) + '/' + str(len(i['subJobInfoVoList'])))

                elif type(w_id) == list:
                    self.A7.append('多后置任务，手动确认')
                    self.A8.append('多后置任务，手动确认')
                    self.A9.append('多后置任务，手动确认')
                    # TODO 处理一个初始人物对应多个后置任务，查询对应对比任务
                else:
                    logger.error('get_compare_task - {}数据错误'.format(w_id))
        except Exception as e:
            logger.error('get_compare_task - 未知错误：{}'.format(e))

    def data(self):
        '''处理数据'''
        try:
            data = []
            data1 = []
            data2 = []

            datas = zip(self.A1,self.A2,self.A3, self.A4, self.A5,self.A6, self.A7, self.A8, self.A9)
            for i in datas:
                data.append(i)
            num = (len(data)/2)
            n = 0
            for j in data:
                if n < num:
                    data1.append(list(j))
                else:
                    data2.append(list(j))
                n += 1
            end_data = [(lambda i: data1.pop() if (data1 != [] and (i % 2 == 0 or data2 == [])) else data2.pop())(i) for i in
                  range(len(data1) + len(data2))]
            logger.info('数据数据函数 - 执行完成')
            return end_data
        except Exception as e:
            logger.error('处理数据函数 - 未知错误:{}'.format(e))

    def is_token(self, token, firedIdList):
        if len(firedIdList) == 1:
            if token == '':
                self.headers['fantasy-token'] = "ZOY/XcnDFYPD3PeL0XF4Md6wWayFCctJCayTM4j8XXsH7ijUqxdQY85vZd4HdYCm4xV434fx0MBjUvQxaWUKprsEaDPfDzkdR5OemIMJIDCISd0dtgsFmqTQTu6nMOxc0c4I/QAZ1q9w3Oxo4E61TG4BvHE+QZBknKHrjGSVRSUnc+sMKllM1UYt+R2GY/tL9ZQBnWPeCLOO7VxxZowN+ZR3/80juRWkClyuOprdfM67ZVtLlvdk5p7e57DqAcm4OrpAp92FnzSXeuSUGCF2qxYhAV2Vjjx2N+d0e/bIUlYNj9cvZCCQLBN1rgirA7DCWDMQIW+ZfiH1rtLTdW58JsINSOxSOGJ4YVTlPyfiEahf3JMLFpSz7MPztT60sCjl"
                logger.info('无token，使用默认token:{}'.format(self.headers['fantasy-token']))
                tkinter.messagebox.showinfo(title='查询', message='开始查：' + firedIdList[0] + ',点击确定后耐心等候。')
            else:
                logger.info('新填写的token:{}'.format(token))
                self.headers['fantasy-token'] = token
                tkinter.messagebox.showinfo(title='查询', message='开始查：' + firedIdList[0] + ',点击确定后耐心等候。')
        else:
            if token == '':
                self.headers['fantasy-token'] = "ZOY/XcnDFYPD3PeL0XF4Md6wWayFCctJCayTM4j8XXsH7ijUqxdQY85vZd4HdYCm4xV434fx0MBjUvQxaWUKprsEaDPfDzkdR5OemIMJIDCISd0dtgsFmqTQTu6nMOxc0c4I/QAZ1q9w3Oxo4E61TG4BvHE+QZBknKHrjGSVRSUnc+sMKllM1UYt+R2GY/tL9ZQBnWPeCLOO7VxxZowN+ZR3/80juRWkClyuOprdfM67ZVtLlvdk5p7e57DqAcm4OrpAp92FnzSXeuSUGCF2qxYhAV2Vjjx2N+d0e/bIUlYNj9cvZCCQLBN1rgirA7DCWDMQIW+ZfiH1rtLTdW58JsINSOxSOGJ4YVTlPyfiEahf3JMLFpSz7MPztT60sCjl"
                logger.info('无token，使用默认token:{}'.format(self.headers['fantasy-token']))
            else:
                logger.info('新填写的token:{}'.format(token))
                self.headers['fantasy-token'] = token

    def file_does_it_exist(self, file_name, data):
        '''判断文件是否存在'''
        file_name = self.path + file_name + '计划信息.xlsx'
        print(file_name)
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
                self.wirte_xlsx(file_name, data)
                return self.wirte_xlsx(file_name, data)
            else:
                self.wirte_xlsx(file_name, data)
                return self.wirte_xlsx(file_name, data)
        except Exception as e:
            return e

    def wirte_xlsx(self, file_name, data_result):
        '''数据导出xlsx'''
        # 实例获取操作页
        # 实例获取操作页
        f = xlwt.Workbook()
        sheet = f.add_sheet('sheet1')

        # 生成表头
        title = ['初始任务ID', '初始任务名', '初始任务结果', '后置任务ID', '后置任务名', '后置任务结果', '对比作业ID', '对比作业任务', '对比作业结果']
        for i in range(len(title)):
            sheet.write(0, 0 + i, title[i])
        # 生成数据
        row = 0
        col = 1
        for list in data_result:
            for j in range(len(list)):
                sheet.write(col, row + j, list[j])
            col += 1

        f.save(file_name)
        result = '数据导出至' + file_name
        logger.info('执行完成，数据导出至：{}'.format(file_name))
        return result

    def main(self):
        '''查计划'''
        logger.info('进入查询流程...')
        # 获取TK传输的值
        u_token = self.entry01.get()
        test_plan_id = self.entry02.get()
        base_plan_id = self.entry03.get()
        if test_plan_id == '' and base_plan_id == '':
            tkinter.messagebox.askokcancel(title='异常', message='必须传入测试计划ID 或 基线计划ID')
            logger.error('gedit:{}'.format('必须传入测试计划ID 或 基线计划ID'))
        elif test_plan_id != '' and base_plan_id == '':
            logger.info('查询计划ID:{}'.format(test_plan_id))
            firedIdList = [test_plan_id]
            for firedId in firedIdList:
                self.is_token(u_token, firedIdList)
                self.get_task_id(firedId)
                self.get_after_job_info()
                self.get_compare_task()
                data = self.data()
                result = self.file_does_it_exist(test_plan_id, data)
                tkinter.messagebox.askokcancel(title='导出结果', message=result)
        elif base_plan_id != '' and test_plan_id == '':
            logger.info('查询计划ID:{}'.format(base_plan_id))
            firedIdList = [base_plan_id]
            for firedId in firedIdList:
                self.is_token(u_token, firedIdList)

                self.get_task_id(firedId)
                self.get_after_job_info()
                self.get_compare_task()
                data = self.data()
                result = self.file_does_it_exist(base_plan_id, data)
                tkinter.messagebox.askokcancel(title='导出结果', message=result)
        else:
            logger.info('查询计划ID:{}&{}'.format(test_plan_id,base_plan_id))
            firedIdList = [test_plan_id, base_plan_id]
            tkinter.messagebox.showinfo(title='查询',
                                        message='开始查：' + firedIdList[0] + ' & ' + firedIdList[1] + ',点击确定后耐心等候。')
            for firedId in firedIdList:
                self.is_token(u_token, firedIdList)
                self.get_task_id(firedId)
            self.get_after_job_info()
            self.get_compare_task()
            data = self.data()
            result = self.file_does_it_exist(test_plan_id+'&'+base_plan_id, data)
            tkinter.messagebox.askokcancel(title='导出结果', message=result)


if __name__ == '__main__':
    root = Tk(className=' WQE-任务查询 ')
    root.geometry("400x170+200+300")
    app = Application(master=root)
    root.mainloop()


