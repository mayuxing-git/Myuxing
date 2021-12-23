import pynput,subprocess,time
from Util.handle_txt import Handle_txt
from Util.handle_log import run_log as logger

class Jb():
    def __init__(self):
        self.ctr = pynput.keyboard.Controller()
        self.jk_min_data = [
            #2
            {'č':['50','67']},{'ď':['50','68']},{'ě':['50','69']},{'ľ':['50','76']},{'ň':['50','78']},{'ř':['50','82']},{'š':['50','83']},{'ť':['50','84']},{'ž':['50','90']},
            #3
            {'â':['51','65']},{'ê':['51','69']},{'î':['51','73']},{'ô':['51','79']},{'û':['51','85']},
            #4
            {'ă':['52','65']},{'ğ':['52','71']},
            #5
            {'å':['53','65']},{'ů':['53','85']},
            #6
            {'ą':['54','65']},{'ę':['54','69']},{'į':['54','73']},{'ų':['54','85']},
            #7
            {'à':['55','65']},{'è':['55','69']},{'ì':['55','73']},{'ò':['55','79']},{'ù':['55','85']},
            # 8
            {'ė':['56','69']},{'ı':['56','73']},{'ż':['56','90']},
            # 9
            {'á':['57','65']},{'ć':['57','67']},{'é':['57','69']},{'í':['57','73']},{'ĺ':['57','76']},{'ń':['57','78']},{'ó':['57','79']},{'ŕ':['57','82']},{'ś':['57','83']},{'ú':['57','85']},{'ý':['57','89']},{'ź':['57','90']},
            # 0
            {'ő':['48','79']},{'ű':['48','85']},
            # -
            {'ä':['187','65']},{'ë':['187','69']},{'ï':['187','73']},{'ö':['187','79']},{'ü':['187','85']},{'ÿ':['187','89']},
            # =
            {'ç':['191','67']},{'ģ':['191','71']},{'ķ':['191','75']},{'ļ':['191','76']},{'ņ':['191','78']},{'ŗ':['191','82']},{'ş':['191','83']},{'ţ':['191','84']},
        ]
        self.jk_max_data = [
            # 2
            {'Č': ['50', '67']}, {'Ď': ['50', '68']}, {'Ě': ['50', '69']}, {'Ľ': ['50', '76']}, {'Ň': ['50', '78']},
            {'Ř': ['50', '82']}, {'Š': ['50', '83']}, {'Ť': ['50', '84']}, {'Ž': ['50', '90']},
            # 3
            {'Â': ['51', '65']}, {'Ê': ['51', '69']}, {'Î': ['51', '73']}, {'Ô': ['51', '79']}, {'Û': ['51', '85']},
            # 4
            {'Ă': ['52', '65']}, {'Ğ': ['52', '71']},
            # 5
            {'Å': ['53', '65']}, {'Ů': ['53', '85']},
            # 6
            {'Ą': ['54', '65']}, {'Ę': ['54', '69']}, {'Į': ['54', '73']}, {'Ų': ['54', '85']},
            # 7
            {'À': ['55', '65']}, {'È': ['55', '69']}, {'Ì': ['55', '73']}, {'Ò': ['55', '79']}, {'Ù': ['55', '85']},
            # 8
            {'Ė': ['56', '69']}, {'İ': ['56', '73']}, {'Ż': ['56', '90']},
            # 9
            {'Á': ['57', '65']}, {'Ć': ['57', '67']}, {'É': ['57', '69']}, {'Í': ['57', '73']}, {'Ĺ': ['57', '76']},
            {'Ń': ['57', '78']}, {'Ó': ['57', '79']}, {'Ŕ': ['57', '82']}, {'Ś': ['57', '83']}, {'Ú': ['57', '85']},
            {'Ý': ['57', '89']}, {'Ź': ['57', '90']},
            # 0
            {'Ő': ['48', '79']}, {'Ű': ['48', '85']},
            # -
            {'Ä': ['187', '65']}, {'Ë': ['187', '69']}, {'Ï': ['187', '73']}, {'Ö': ['187', '79']},
            {'Ü': ['187', '85']}, {'Ÿ': ['187', '89']},
            # =
            {'Ç': ['191', '67']}, {'Ģ': ['191', '71']}, {'Ķ': ['191', '75']}, {'Ļ': ['191', '76']},
            {'Ņ': ['191', '78']}, {'Ŗ': ['191', '82']}, {'Ş': ['191', '83']}, {'Ţ': ['191', '84']},
        ]
        self.bl_min_data = [
            {'ě':['50','69']},{'ř':['50','82']},{'ž':['50','90']},{'ť':['50','84']},{'š':['50','83']},{'ď':['50','68']},{'č':['50','67']},{'ň':['50','78']},
            {'î': ['51', '73']},{'ô': ['51', '67']},{'â': ['51', '65']},
            {'ă': ['52', '65']},
            {'ů': ['53', '85']},
            {'ą': ['54', '65']},{'ę': ['54', '69']},
            {'ż': ['56', '90']},
            {'é': ['57', '69']},{'ŕ': ['57', '82']},{'ź': ['57', '90']},{'ú': ['57', '85']},{'í': ['57', '73']},{'ó': ['57', '67']},{'á': ['57', '65']},{'ś': ['57', '83']},{'ĺ': ['57', '73']},{'ý': ['57', '89']},{'ć': ['57', '67']},{'ń': ['57', '78']},
            {'ű': ['48', '85']},{'ő': ['48', '79']},
            {'ë': ['187', '69']},{'ü': ['48', '85']},{'ö': ['48', '79']},{'ä': ['48', '65']},
            {'ţ': ['191', '84']},{'ş': ['48', '83']},{'ç': ['48', '67']},
        ]
        self.bl_max_data = [
            {'Ě': ['50', '69']}, {'Ř': ['50', '82']}, {'Ž': ['50', '90']}, {'Ť': ['50', '84']}, {'Š': ['50', '83']},
            {'Ď': ['50', '68']}, {'Č': ['50', '67']}, {'Ň': ['50', '78']},
            {'Î': ['51', '73']}, {'Ô': ['51', '67']}, {'Â': ['51', '65']},
            {'Ă': ['52', '65']},
            {'Ů': ['53', '85']},
            {'Ą': ['54', '65']}, {'Ę': ['54', '69']},
            {'Ż': ['56', '90']},
            {'É': ['57', '69']}, {'Ŕ': ['57', '82']}, {'Ź': ['57', '90']}, {'Ú': ['57', '85']}, {'Í': ['57', '73']},
            {'Ó': ['57', '67']}, {'Á': ['57', '65']}, {'Ś': ['57', '83']}, {'Ĺ': ['57', '73']}, {'Ý': ['57', '89']},
            {'Ć': ['57', '67']}, {'Ń': ['57', '78']},
            {'Ű': ['48', '85']}, {'Ő': ['48', '79']},
            {'Ë': ['187', '69']}, {'Ü': ['48', '85']}, {'Ö': ['48', '79']}, {'Ä': ['48', '65']},
            {'Ţ': ['191', '84']}, {'Ş': ['48', '83']}, {'Ç': ['48', '67']},
        ]
    def run_mian(self,num):
        subprocess.Popen('ceshi.txt', shell=True)
        time.sleep(2)
        Handle_txt().clear_data()
        Handle_txt().save_data()

        time.sleep(5)
        if int(num) == 1:
            print('预测验，微软输入法某些按键均能响应')
            title = '捷克语组合'
            # 小写组合
            Jb().test_min_case(title, self.jk_min_data)
            # 大写组合
            Jb().test_max_case(title, self.jk_max_data)
        elif int(num) == 2:
            title = '波兰语组合'
            print('预测验，微软输入法某些按键不能响应')
            Jb().test_min_case(title,self.bl_min_data)
        else:
            print('退出测验')

    def test_min_case(self,title,data):
        logger.info('{}-小写组合'.format(title))
        for keys in data:
            for key, value in keys.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(18))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(18))

                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                #  space     enter
                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)

                result = self.txt()
                if result.split(' ')[0] == key:
                    break
                else:
                    logger.error('匹配错误:预期 右alt+{}+{}->{}  上屏->{}'.format(value[0],value[1],key,result))
    def test_max_case(self,title,data):
        logger.info('{}-大写组合'.format(title))
        for keys in data:
            for key, value in keys.items():
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(18))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[0])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(17))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(18))

                self.ctr.press(pynput.keyboard.KeyCode.from_vk(16))
                self.ctr.press(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(int(value[1])))
                self.ctr.release(pynput.keyboard.KeyCode.from_vk(16))
                #  space     enter
                self.ctr.press(pynput.keyboard.Key.space)
                self.ctr.release(pynput.keyboard.Key.space)

                result = self.txt()
                if result.split(' ')[0] == key:
                    break
                else:
                    logger.error('匹配错误:预期 右alt+{}+{}->{}  上屏->{}'.format(value[0],value[1],key,result))


    def txt(self):
        Handle_txt().save_data()
        Handle_txt().clear_data()
        with open('ceshi.txt', 'r', encoding='utf-8') as f:
            return f.read()

if __name__ == '__main__':
    print('1-> 捷克语组合； 2-> 波兰语组合')
    num = 2
    Jb().run_mian(num)

