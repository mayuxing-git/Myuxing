import pymouse

# 'sogou' 'xunfei' 'huayu' 'baidu'
INPUT = 'sogou'
# ubuntu: 'gedit', kylin: 'pluma', UOS: 'deepin-editor'
EDIT = 'deepin-editor'
PARAMS = {
    'sogou': {
        'candarea': {
            'top': 0.5,
            'bottom': 0.93,
            'left': 0.02,
            'right': 0.825
        },
        'pinyin_dict_button': (0.1, 0.530),
        'pinyin_clear_button': (0.471, 0.609),
        'wubi_dict_button': (0.1, 0.622),
        'wubi_clear_button': (0.478, 0.807)
    },
    'sogou_virtual_keyboard': {
        'candarea': {
            'top': 0.059,
            'bottom': 0.196,
            'left': 0.0,
            'right': 0.909
        },
        'switch_keyboard': (0.273, 0.095),
        '9key': (0.229, 0.384),
        '26key': (0.5, 0.384),
        '26key_eng': (0.767, 0.755),
        'shift_26': (0.080, 0.691),
        'backspace_9': (0.894, 0.299),
        'enter_9': (0.894, 0.889),
        'space_9': (0.486, 0.889),
        'backspace_26': (0.918, 0.691),
        'enter_26': (0.918, 0.889),
        'space_26': (0.5, 0.889),
        'dict_name': ['sgim_en_usr.bin', 'sgim_gd_s3_usrbg.bin', 'sgim_gd_s4_usrbg.bin', 'sgim_gd_umusr.bin', 'sgim_gd_usr.bin'],
        'pinyin_9key_btn_pos_info': {
            'key_btn_pos': {
                '1': (0.287, 0.299),
                '4': (0.287, 0.5),
                '7': (0.287, 0.696),
            },
            'interval': 0.203
        },
        'pinyin_26key_btn_pos_info': {
            'key_btn_pos': {
                'q': (0.056, 0.302),
                'a': (0.106, 0.5),
                'z': (0.205, 0.691),
            },
            'interval': 0.098
        }
    },
    'xunfei': {
        'status_window_name': 'Form',
        'candarea': {
            'top': 0.555,
            'bottom': 0.889,
            'left': 0.012,
            'right': 0.78
        },
        'handinput_btn': (0.725, 0.5),
        'pinyin_dict_button': (0.127, 0.351),
        'pinyin_clear_button': (0.396, 0.255),
        'pinyin_clear_enter_button': (0.34375, 0.866),
        'open_config_window': (0.5, 0.558),
        'close_config_window': (0.954, 0.062)
    },
    'huayu': {},
    'baidu': {}
}

M = pymouse.PyMouse()
