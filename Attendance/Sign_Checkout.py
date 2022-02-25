import requests, re, time, xlwt, os

class Om_Attendance():
    def __init__(self):
        self.time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.year = self.time.split('-')[0]
        self.month = str(int(self.time.split('-')[1])-1)
        self.day = ['1','8','15','22','29','31']
        # self.day = ['23']
        self.url = ''
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Cookie': ''
        }
        self.list = []
    def get_data(self):
        '''获取考勤数据'''
        for day in self.day:
            url = self.url + self.year +'-'+ self.month +'-'+ day
            response = requests.get(url=url, headers=self.headers)
            text = response.text.replace('\n','').replace('"','').replace("'",'').replace('\t','').replace('&nbsp;','')\
                .replace('<td class=pad_space>', ',<td class=pad_space>').split(',')
            text.reverse() # 倒叙排列
            text.pop()     # 删除多余数据

            print(text)
            for i in text:
                dic = {}
                dic['month'] = self.month
                dic['name'] = '马宇星'

                dic['data'] = str(re.findall(">(.*?)'",str(re.findall('<td class=pad_space><span class=(.*?)<',i)))[0])
                dic['to_time'] =str(re.findall(">(.*?)'",str(re.findall('<td class=pad_space><span class=(.*?)<',i)))[0]).split(' ')[0] +\
                                '  ' + str(re.findall('<td>(.*?)</td>',i)[0])
                dic['out_time'] = str(re.findall(">(.*?)'",str(re.findall('<td class=pad_space><span class=(.*?)<',i)))[0]).split(' ')[0] +\
                                  '  ' + str(re.findall('<td>(.*?)</td>',i)[2])
                dic['total_time'] = str(re.findall('>(.*?)<', str(re.findall('<td>(.*?)</td>', i)[4]))).replace('[','').replace(']','').replace("'",'')

                if dic['data'].split(' ')[0].split('-')[1] == self.month:
                    self.list.append(dic)

        self.write_excel()
    def write_excel(self):
        path = 'C:/Users/mayuxing/Desktop/'
        file_name = path + self.month + '月份考勤.xlsx'
        # 实例获取操作页
        f = xlwt.Workbook()
        sheet = f.add_sheet('sheet1')
        # 生成表头
        title = ['月份','姓名','日期','签到时间','签出时间','考勤总时长','餐补','车补','备注']
        for i in range(len(title)):
            sheet.write(0,0+i,title[i])
        # 生成数据
        row = 0
        col = 1
        for dic in self.list:
            for j in range(len(list(dic.values()))):
                sheet.write(col, row + j+2, list(dic.values())[j])
            col += 1
        sheet.write_merge(1,len(self.list),0,0,self.month + '月份')
        sheet.write_merge(1, len(self.list), 1, 1, '马宇星')
        f.save(file_name)

Om_Attendance().get_data()
