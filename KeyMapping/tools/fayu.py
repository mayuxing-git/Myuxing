import pynput,subprocess,time
from Util.handle_txt import Handle_txt
from Util.handle_log import run_log as logger

class Fayu():
    def __init__(self):
        self.ctr = pynput.keyboard.Controller()
        self.min_data = [
            [{'à':['192','65']},{'è':['192','69']},{'ì':['192','73']},{'ò':['192','79']},{'ù':['192','85']},{'â':['219','65']}, {'ê':['219','69']},{'î':['219','73']},{'ô':['219','79']},{'û':['219','85']},{'ç':['221','67']},],
            [{'á':['220','65']},{'é':['220','69']},{'í':['220','73']},{'ó':['220','79']},{'ú':['220','85']},{'ý':['220','89']},],
            [{'ä':['221','65']},{'ë':['221','69']},{'ï':['221','73']},{'ö':['221','79']},{'ü':['221','85']},{'ÿ':['221','89']},],
        ]
        self.max_data = [
            [{'À': ['192', '65']}, {'È': ['192', '69']}, {'Ì': ['192', '73']}, {'Ò': ['192', '79']}, {'Ò': ['192', '85']}, {'Â': ['219', '65']}, {'Ê': ['219', '69']}, {'Î': ['219', '73']}, {'Ô': ['219', '79']}, {'Û': ['219', '85']}, {'Ç': ['221', '67']}, ],
            [{'Á': ['220', '65']}, {'É': ['220', '69']}, {'Í': ['220', '73']}, {'Ó': ['220', '79']},{'Ú': ['220', '85']}, {'Ý': ['220', '89']}, ],
            [{'Ä': ['221', '65']}, {'Ë': ['221', '69']}, {'Ï': ['221', '73']}, {'Ö': ['221', '79']},{'Ü': ['221', '85']}, {'Ÿ': ['221', '89']}, ],
        ]

    def run_mian(self):
        # subprocess.Popen('ceshi.txt', shell=True)
        # time.sleep(2)
        # Handle_txt().clear_data()
        # Handle_txt().save_data()
        # time.sleep(5)
        #
        self.test_min_data()
        time.sleep(1)
        self.test_max_data()

    def test_min_data(self):
        logger.info('法语小写组合')
        for data in self.min_data[0]:
            print(data)

        for data in self.min_data[1]:
            print(data)

        for data in self.min_data[2]:
            print(data)

    def test_max_data(self):
        logger.info('法语大写组合')
        for data in self.min_data[0]:
            print(data)

        for data in self.min_data[1]:
            print(data)

        for data in self.min_data[2]:
            print(data)

    def txt(self):
        Handle_txt().save_data()
        Handle_txt().clear_data()
        with open('ceshi.txt', 'r', encoding='utf-8') as f:
            return f.read()

if __name__ == '__main__':
    Fayu().run_mian()