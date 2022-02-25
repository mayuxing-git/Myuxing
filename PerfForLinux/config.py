import pymouse

# 'sogou' 'xunfei' 'huayu' 'baidu'
INPUT = 'sogou'
# ubuntu: 'gedit', kylin: 'pluma', UOS: 'deepin-editor'
EDIT = 'deepin-editor'
# 'pinyin_input' 'hand_input' 'virtual_input'
KEYBOARD_TYPE = 'pinyin_input'
PARAMS = {
    'sogou': {
        'candarea': {
            'top': 0.5,
            'bottom': 0.93,
            'left': 0.02,
            'right': 0.825
        },
        'editor_first_word': {
            'top': 0.0741,
            'bottom': 0.1105,
            'left': 0.0389,
            'right': 0.056
        },
        'handinput_grab_time_interval': 0.001,
        #'voice_input_button': (0.828, 0.5),#2.1
        'voice_input_button': (0.728, 0.5),
        'voice_input_close_button': (0.832, 0.135),
        'pinyin_dict_button': (0.1, 0.530),
        'pinyin_clear_button': (0.471, 0.609),
        'wubi_dict_button': (0.1, 0.622),
        'wubi_clear_button': (0.478, 0.807),
        'handinput_area': {
            'top': 0.267,
            'bottom': 0.765,
            'left': 0.081,
            'right': 0.780
        },
        'handinput_candarea': {
            'top': 0.117,
            'bottom': 0.216,
            'left': 0.037,
            'right': 0.966
        },
        #'handinput_btn': (0.726, 0.5),#2.1
        'handinput_btn': (0.576, 0.5),#2.3
        'handinput_close': (0.960, 0.061),
        'interval': 59,
        'ime_service_name': 'sogouImeService',
        'handinput_service_name': 'SogouHandInput',
        'virtual_keyboard': {
            'first_cand_pos': 0.042,
            'cand_area_top': 0.059,
            'cand_area': (0.909, 0.196),
            'switch_keyboard': (0.273, 0.095),
            '9key': (0.229, 0.384),
            '26key': (0.5, 0.384),
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
        'editor_first_word': {
            'top': 0.0741,
            'bottom': 0.1105,
            'left': 0.0389,
            'right': 0.056
        },
        'voice_input_button': (0.6175, 0.5),
        'voice_input_close_button': (0.956, 0.101),
        'handinput_btn': (0.725, 0.5),
        'handinput_close': (0.954, 0.045),
        'handinput_grab_time_interval': 0.001,
        'single_word_handinput_btn': (0.054, 0.186),
        'multi_word_handinput_btn': (0.054, 0.369),
        'first_cand_handinput_area': {
            'top': 0.096,
            'bottom': 0.408,
            'left': 0.657,
            'right': 1
        },
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
    },
    'huayu': {},
    'baidu': {}
}

M = pymouse.PyMouse()
