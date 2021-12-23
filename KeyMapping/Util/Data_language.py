from Util.handle_ini import Handle_ini
from Test_data.data import Testdata
import ast


def keyboard(layouts,datas):
    '''以键盘按键为基础：四排按键，分别获取每个布局下的按键数据'''

    lists = []
    for i in range(len(layouts)):
        list = []
        for data in datas:
            list.append(data[i])
        lists.append(list)
    return lists

def test_data():
    ''' 判断测试哪种语言 return ： 测试数据（四排键盘） 布局  上屏方式'''
    language = Handle_ini().get_value('language', 'test_data')

    if int(language.split('.')[0]) == 0:
        title = '《中文 字母》数据'
        testdata = list(Testdata().china())
        layout = list(ast.literal_eval(Handle_ini().get_value('china', 'model')))[0]
        way = int(list(ast.literal_eval(Handle_ini().get_value('china', 'model')))[1])
        label = False
        return title, testdata, layout, way, label

    elif int(language.split('.')[0]) == 1:
        if int(language.split('.')[1]) == 0:
            title = '《韩语》数据'
            # 获取该语言的测试数据
            testdata = list(Testdata().hy())
            # 获取该语言有几种布局
            layout = list(ast.literal_eval(Handle_ini().get_value('hanyu', 'model')))[0]
            # 获取该语言合适的上屏方式
            way = int(list(ast.literal_eval(Handle_ini().get_value('hanyu', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        else:
            return '错误：检查{0}数据是否存在'.format(language)
    elif int(language.split('.')[0]) == 2:
        if int(language.split('.')[1]) == 0:
            title = '《藏语》数据'
            testdata = list(Testdata().zy())
            layout = list(ast.literal_eval(Handle_ini().get_value('zangyu', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('zangyu', 'model')))[1])
            label = True
            return title, testdata, layout, way, label
        else:
            return '错误：检查{0}数据是否存在'.format(language)

    elif int(language.split('.')[0]) == 3:
        if int(language.split('.')[1]) == 1:
            title = '《日语Romaji_hiragana》数据'
            testdata = list(Testdata().ry_r_hiragana())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_r_hiragana', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_r_hiragana', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[1]) == 2:
            title = '《日语Romaji_f_katakana》数据'
            testdata = list(Testdata().ry_r_f_katakana())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_r_f_katakana', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_r_f_katakana', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[1]) == 3:
            title = '《日语Romaji_f_aiphanumeric》数据'
            testdata = list(Testdata().ry_r_f_aiphanumeric())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_r_f_aiphanumeric', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_r_f_aiphanumeric', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[1]) == 4:
            title = '《日语Romaji_h_katakana》数据'
            testdata = list(Testdata().ry_r_h_katakana())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_r_h_katakana', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_r_h_katakana', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[1]) == 5:
            title = '《日语Romaji_h_aiphanumeric》数据'
            testdata = list(Testdata().ry_r_h_aiphanumeric())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_r_h_aiphanumeric', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_r_h_aiphanumeric', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        else:
            return '错误：检查{0}数据是否存在'.format(language)

    elif int(language.split('.')[0]) == 4:
        if int(language.split('.')[0]) == 4 and int(language.split('.')[1]) == 1:
            title = '《日语Kana_hiragana》数据'
            testdata = list(Testdata().ry_k_hiragana())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_k_hiragana', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_k_hiragana', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[0]) == 4 and int(language.split('.')[1]) == 2:
            title = '《日语Kana_f_katakana》数据'
            testdata = list(Testdata().ry_k_f_katakana())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_k_f_katakana', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_k_f_katakana', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[0]) == 4 and int(language.split('.')[1]) == 3:
            title = '《日语Kana_f_aiphanumeric》数据'
            testdata = list(Testdata().ry_k_f_aiphanumeric())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_k_f_aiphanumeric', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_k_f_aiphanumeric', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[0]) == 4 and int(language.split('.')[1]) == 4:
            title = '《日语Kana_h_katakana》数据'
            testdata = list(Testdata().ry_k_h_katakana())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_k_h_katakana', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_k_h_katakana', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        elif int(language.split('.')[0]) == 4 and int(language.split('.')[1]) == 5:
            title = '《日语Kana_h_aiphanumeric》数据'
            testdata = list(Testdata().ry_k_h_aiphanumeric())
            layout = list(ast.literal_eval(Handle_ini().get_value('ry_k_h_aiphanumeric', 'model')))[0]
            way = int(list(ast.literal_eval(Handle_ini().get_value('ry_k_h_aiphanumeric', 'model')))[1])
            label = False
            return title, testdata, layout, way, label
        else:
            return '错误：检查{0}数据是否存在'.format(language)
    elif int(language.split('.')[0]) == 5:
        title = '《捷克语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().jieke())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('jieke', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('jieke', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 6:
        title = '《波兰语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().bolan())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('bolan', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('bolan', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 7:
        title = '《瑞典语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().ruidian())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('ruidian', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('ruidian', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 8:
        title = '《克罗地亚语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().keluodiya())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('keluodiya', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('keluodiya', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 9:
        title = '《法语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().fayu())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('fayu', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('fayu', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 10:
        title = '《罗马尼亚语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().luomaniya())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('luomaniya', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('luomaniya', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 11:
        title = '《泰语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().taiyu())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('taiyu', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('taiyu', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 12:
        title = '《印地语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().yindi())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('yindi', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('yindi', 'model')))[1])
        label = False
        return title, testdata, layout, way, label

    elif int(language.split('.')[0]) == 13:
        title = '《丹麦语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().danmai())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('danmai', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('danmai', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 14:
        title = '《塞尔维亚语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().saierweiya())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('saierweiya', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('saierweiya', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    elif int(language.split('.')[0]) == 15:
        title = '《匈牙利语》数据'
        # 获取该语言的测试数据
        testdata = list(Testdata().xiongyali())
        # 获取该语言有几种布局
        layout = list(ast.literal_eval(Handle_ini().get_value('xiongyali', 'model')))[0]
        # 获取该语言合适的上屏方式
        way = int(list(ast.literal_eval(Handle_ini().get_value('xiongyali', 'model')))[1])
        label = False
        return title, testdata, layout, way, label
    else:
        return '错误：检查{0}数据是否存在'.format(language)