import pymouse

# 'sogou' 'xunfei' 'huayu' 'baidu'
INPUT = 'sogou'
# ubuntu: 'gedit', kylin: 'pluma', UOS: 'deepin-editor'
EDIT = 'deepin-editor'
PARAMS = {
    'sogou': {
        'candarea': {
            'top': 0.117,
            'bottom': 0.216,
            'left': 0.037,
            'right': 0.966
        },
        'handinput_area': {
            'top': 0.267,
            'bottom': 0.765,
            'left': 0.081,
            'right': 0.780
        },
        'handinput_grab_time_interval': 0.001,
        'isneed_response_time': True,
        'interval': 59,
        'handinput_btn': (0.576, 0.5),
        #'handinput_btn': (0.726, 0.5),
        'handinput_close': (0.960, 0.061),
        'handinput_default_cand_num': 10,
        'pinyin_dict_button': (0.1, 0.530),
        'pinyin_clear_button': (0.471, 0.609),
        'wubi_dict_button': (0.1, 0.622),
        'wubi_clear_button': (0.478, 0.807),
        'ime_service_name': 'sogouImeService'
    },
    'xunfei': {
        'status_window_name': 'Form',
        'handinput_btn': (0.726, 0.5),
        'single_word_handinput_btn': (0.054, 0.186),
        'multi_word_handinput_btn': (0.054, 0.369),
        'single_word_handinput_area': {
            'top': 0.233,
            'bottom': 0.808,
            'left': 0.153,
            'right': 0.622
        },
        'single_word_candarea': {
            'top': 0.412,
            'bottom': 0.714,
            'left': 0.657,
            'right': 1
        },
        'single_word_rewrite': {
            'x': 0.326,
            'y': 0.889
        },
        'multi_word_handinput_area': {
            'top': 0.359,
            'bottom': 0.822,
            'left': 0.175,
            'right': 0.853
        },
        'multi_word_cand_area': {
            'top': 0.097,
            'bottom': 0.209,
            'left': 0.11,
            'right': 1
        },
        'double_word_rewrite': {
            'x': 0.977,
            'y': 0.5
        },
        'handinput_grab_time_interval': 0.001,
        'isneed_response_time': True,
        'handinput_close': (0.954, 0.045)
    },
    'huayu': {},
    'baidu': {}
}

M = pymouse.PyMouse()
