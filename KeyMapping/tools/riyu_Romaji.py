import pynput,subprocess,time
from Util.handle_txt import Handle_txt

def romaji_01(data1,ctr):
    list1 = {'':'','k':'75','s':'83','t':'84','n':'78','h':'72','m':'77','y':'89','r':'82','w':'87',}
    list2 = {'a':'65','i':'73','u':'85','e':'69','o':'79',}

    yuan = list(list1.values())
    fu = list(list2.values())

    x= 0
    for i in yuan:
        for j in fu:
            if i=='89' and j=='73':
                # print('y+i == 0')
                b = 0
                y = [key for key, vlaues in list1.items() if vlaues == i]
                f = [key for key, vlaues in list2.items() if vlaues == j]
                a = '+'.join(y + f)
                handle_txt(a, x,b)
            elif i == '89'and j=='69':
                # print('y+e == 0')
                b = 0
                y = [key for key, vlaues in list1.items() if vlaues == i]
                f = [key for key, vlaues in list2.items() if vlaues == j]
                a = '+'.join(y + f)
                handle_txt(a, x,b)
            elif i == '87' and j == '73':
                # print('w+i == 0')
                b = 0
                y = [key for key, vlaues in list1.items() if vlaues == i]
                f = [key for key, vlaues in list2.items() if vlaues == j]
                a = '+'.join(y + f)
                handle_txt(a, x,b)

            elif i == '87' and j == '85':
                # print('w+u == 0')
                b = 0
                y = [key for key, vlaues in list1.items() if vlaues == i]
                f = [key for key, vlaues in list2.items() if vlaues == j]
                a = '+'.join(y + f)
                handle_txt(a, x,b)
            elif i == '87' and j == '69':
                # print('w+e == 0')
                b = 0
                y = [key for key, vlaues in list1.items() if vlaues == i]
                f = [key for key, vlaues in list2.items() if vlaues == j]
                a = '+'.join(y + f)
                handle_txt(a, x,b)
            else:

                if i == '':
                    ctr.press(pynput.keyboard.KeyCode.from_vk(int(j)))
                    ctr.release(pynput.keyboard.KeyCode.from_vk(int(j)))

                    ctr.press(pynput.keyboard.KeyCode.from_vk(13))
                    ctr.release(pynput.keyboard.KeyCode.from_vk(13))

                else:
                    ctr.press(pynput.keyboard.KeyCode.from_vk(int(i)))
                    ctr.release(pynput.keyboard.KeyCode.from_vk(int(i)))
                    time.sleep(0.5)
                    ctr.press(pynput.keyboard.KeyCode.from_vk(int(j)))
                    ctr.release(pynput.keyboard.KeyCode.from_vk(int(j)))

                    ctr.press(pynput.keyboard.KeyCode.from_vk(13))
                    ctr.release(pynput.keyboard.KeyCode.from_vk(13))

                Handle_txt().save_data()
                Handle_txt().clear_data()
                with open('../Main_process/ceshi.txt', 'r', encoding='utf-8') as f:
                    b = f.read()
            y = [key for key,vlaues in list1.items() if vlaues==i]
            f = [key for key,vlaues in list2.items() if vlaues==j]
            a = '+'.join(y+f)
            x += 1

            # data :默认数据  a ：按下的键  b：屏上的值
            handle_txt(data1,a,x,b)



def handle_txt(data,a,x,b=None,):

    if b == None:
        print('{}={} -> {}**********************'.format(a,data[x-1],b))
    else:
        try:
            if b == data[x-1]:
                print('匹配正确:{}={} -> {}'.format(a,data[x-1],b))
        except Exception as e:
            print(e)



if __name__ == '__main__':

    data1 = [
        'あ', 'い', 'う', 'え', 'お',
        'か', 'き', 'く', 'け', 'こ',
        'さ', 'し', 'す', 'せ', 'そ',
        'た', 'ち', 'つ', 'て', 'と',
        'な', 'に', 'ぬ', 'ね', 'の',
        'は', 'ひ', 'ふ', 'へ', 'ほ',
        'ま', 'み', 'む', 'め', 'も',
        'や', '', 'ゆ', '', 'よ',
        'ら', 'り', 'る', 'れ', 'ろ',
        'わ', '', '', '', 'を',
    ]
    data2 = [
        'ア', 'イ', 'ウ', 'エ', 'オ',
        'カ', 'キ', 'ク', 'ケ', 'コ',
        'サ', 'シ', 'ス', 'セ', 'ソ',
        'タ', 'チ', 'ツ', 'テ', 'ト',
        'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
        'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
        'マ', 'ミ', 'ム', 'メ', 'モ',
        'ヤ', '', 'ユ',' ', 'ヨ',
        'ラ', 'リ', 'ル', 'レ', 'ロ',
        'ワ', '', '', '', 'ヲ',
    ]
    ctr = pynput.keyboard.Controller()

    subprocess.Popen('ceshi.txt', shell=True)
    time.sleep(2)
    Handle_txt().clear_data()
    Handle_txt().save_data()
    time.sleep(10)

    #   罗马映射：data1：  data2：
    romaji_01(data1,ctr)
