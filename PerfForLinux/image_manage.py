import numpy as np
import cv2
from mss import mss
import time
from window_impl import get_status_box_geometry, get_handinput_window, get_virtual_keyboard_geometry, \
    get_voiceinput_geometry
from keys import do, shift, ctrl
from config import INPUT, PARAMS, M
import os

box = {'top': 100, 'left': 100, 'width': 50, 'height': 60}
sct = mss()
result = []
result_hash = []


def get_grab_frame(bounding_box, interval, px=10, py=10):
    start = time.time()
    result.clear()
    count = 0
    while True:
        sct_img = sct.grab(bounding_box)
        img = cv2.resize(np.array(sct_img), (px, py), interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result.append(gray)
        count = count + 1
        time.sleep(0.002)
        if time.time() - start > interval:
            break
    return count


def get_hash(data):
    hash_str = ''
    sum = 0
    count = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            sum = sum + data[i][j]
            count = count + 1
    avg = int(sum / count)
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 返回值为True: 表示不相似
def cmp_hash(hash1, hash2, threshold=10):
    n = 0
    if len(hash1) != len(hash2):
        return False
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    if n < threshold:
        return False
    else:
        # print(n)
        return True


def get_status_box_time(box):
    interval = 1
    do(ctrl + shift)
    count = get_grab_frame(box, interval)
    do(ctrl + shift)
    time.sleep(1)
    image_count = 0
    result_hash.clear()
    for i in range(len(result)):
        result_hash.append(get_hash(result[i]))
    for i in range(len(result_hash) - 1):
        if cmp_hash(result_hash[i], result_hash[i + 1], 10):
            # print('i: ' + str(i))
            image_count = i + 2
            break
    if not image_count:
        return -1
    res = int(1000 * interval * image_count / count)
    return res


def get_handinput_box_time(name, img_box):
    interval = 3
    geom = get_status_box_geometry(name)
    time.sleep(0.01)
    click_button = (int(geom.x + geom.width * PARAMS[INPUT]['handinput_btn'][0]),
                    int(geom.y + geom.height * PARAMS[INPUT]['handinput_btn'][1]))
    M.click(click_button[0], click_button[1])

    count = get_grab_frame(img_box, interval)
    time.sleep(1)
    box = get_handinput_window()
    click_button = (int(box.x + box.width * PARAMS[INPUT]['handinput_close'][0]),
                    int(box.y + box.height * PARAMS[INPUT]['handinput_close'][1]))
    M.click(click_button[0], click_button[1])
    time.sleep(1)
    image_count = 0
    result_hash.clear()
    print('result:' + str(len(result)))
    for i in range(len(result)):
        result_hash.append(get_hash(result[i]))
    for i in range(len(result_hash) - 1):
        if cmp_hash(result_hash[i], result_hash[i + 1], 1):
            # print('i: ' + str(i))
            image_count = i + 2
            break
    if not image_count:
        return -1
    res = int(1000 * interval * image_count / count)
    return res


def get_voiceinput_window_box(name):
    geom = get_status_box_geometry(name)
    time.sleep(0.01)
    open_voiceinput_button = (int(geom.x + geom.width * PARAMS[INPUT]['voice_input_button'][0]),
                              int(geom.y + geom.height * PARAMS[INPUT]['voice_input_button'][1]))
    M.click(open_voiceinput_button[0], open_voiceinput_button[1])
    time.sleep(1)
    voice_window_box = get_voiceinput_geometry()
    close_voiceinput_button = (int(voice_window_box.x + voice_window_box.width * PARAMS[INPUT]['voice_input_close_button'][0]),
                               int(voice_window_box.y + voice_window_box.height * PARAMS[INPUT]['voice_input_close_button'][1]))
    M.click(close_voiceinput_button[0], close_voiceinput_button[1])
    time.sleep(1)
    return voice_window_box


def get_voiceinput_box_time(name, img_box):
    interval = 3
    geom = get_status_box_geometry(name)
    time.sleep(0.01)
    open_voiceinput_button = (int(geom.x + geom.width * PARAMS[INPUT]['voice_input_button'][0]),
                              int(geom.y + geom.height * PARAMS[INPUT]['voice_input_button'][1]))
    M.click(open_voiceinput_button[0], open_voiceinput_button[1])

    count = get_grab_frame(img_box, interval)
    time.sleep(1)
    voice_window_box = get_voiceinput_geometry()
    close_voiceinput_button = (int(voice_window_box.x + voice_window_box.width *
                                   PARAMS[INPUT]['voice_input_close_button'][0]),
                               int(voice_window_box.y + voice_window_box.height *
                                   PARAMS[INPUT]['voice_input_close_button'][1]))
    M.click(close_voiceinput_button[0], close_voiceinput_button[1])
    time.sleep(1)
    image_count = 0
    result_hash.clear()
    print('result:' + str(len(result)))
    for i in range(len(result)):
        result_hash.append(get_hash(result[i]))
    for i in range(len(result_hash) - 1):
        if cmp_hash(result_hash[i], result_hash[i + 1], 1):
            # print('i: ' + str(i))
            image_count = i + 2
            break
    if not image_count:
        return -1
    res = int(1000 * interval * image_count / count)
    return res


def get_virtual_keyboard_box_time(box):
    interval = 1
    do(ctrl + shift)
    count = get_grab_frame(box, interval)
    do(ctrl + shift)
    time.sleep(1)
    image_count = 0
    result_hash.clear()
    for i in range(len(result)):
        result_hash.append(get_hash(result[i]))
    for i in range(len(result_hash) - 1):
        if cmp_hash(result_hash[i], result_hash[i + 1], 10):
            print('i: ' + str(i))
            image_count = i + 2
            break
    if not image_count:
        return -1
    res = int(1000 * interval * image_count / count)
    return res


def get_press_key_response_time(box):
    interval = 1
    count = get_grab_frame(box, interval, 20, 20)
    time.sleep(0.05)
    image_count = 0
    print('count: ' + str(count))
    result_hash.clear()
    for i in range(len(result)):
        result_hash.append(get_hash(result[i]))
    left = 0
    right = len(result) - 1
    while left != right - 1:
        mid = (left + right) // 2
        cmp_res = cmp_hash(result_hash[left], result_hash[mid], 1)
        if cmp_res:
            right = mid
        else:
            left = mid
    if cmp_hash(result_hash[left], result_hash[right], 1):
        print('cmp: ' + str(left))
        image_count = left + 2
    # for i in range(len(result_hash) - 1):
    #     if cmp_hash(result_hash[i], result_hash[i + 1], 1):
    #         print('i: ' + str(i))
    #         image_count = i + 2
    #         break
    if not image_count:
        return -1
    res = int(1000 * interval * image_count / count)
    return res


if __name__ == '__main__':
    geom = get_status_box_geometry('Sogou')
    box['top'] = geom.y
    box['left'] = geom.x
    box['width'] = geom.width
    box['height'] = geom.height
    os.popen('deepin-editor')
    time.sleep(1)
    res = get_status_box_time(box)
    print(res)
