# coding=utf-8
'''读取配置文件'''

import sys, os
import configparser

curPath = os.path.abspath(os.path.dirname(__file__))
BasePath = curPath[:curPath.find("") - len("Util")]

from Util.handle_log import run_log as logger

class Handle_ini():

    def load_ini(self):
        '''获取配置文件内容'''
        file_path = BasePath + '/Config/config.ini'
        #使配置文件生效
        cf = configparser.ConfigParser()
        cf.read(file_path,encoding='utf-8')
        return cf

    def get_value(self,key,node=None):
        '''获取配置文件内具体值'''
        if node == None:
            node = 'TEST'
        cf = self.load_ini()

        try:
            data = cf.get(node,key)
            # logger.info('测试 -> 获取配置文件的值-成功：node：{} -> key:{} -> data:{}'.format(node,key,data))
        except Exception as e:
            # logger.exception('测试 -> 获取配置文件的值-失败，node：{} -> key：{} -> error:{}'.format(node, key,e))
            data = None
        return data

#　自调试
# handle_ini = HanleIni()
# if __name__ == '__main__':
#     HanleIni().get_value('language','test_data')