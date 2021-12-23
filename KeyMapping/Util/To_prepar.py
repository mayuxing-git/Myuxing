import time
def to_prepar(title):
    '''延时 准备'''
    ks = 0
    for i in range(10):
        time.sleep(1)
        print('程序还有《{0}》秒开始,需手动切换至：   {1}   模式'.format(10 - i, title))
        ks += 1
        if ks == 10:
            break
