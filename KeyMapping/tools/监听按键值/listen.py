# 监听键盘
from pynput import keyboard
def on_press(key):
    '''按下按键时执行'''
    # 通过属性判断按键类型。
    try:
        print('按下字母数字键{0}'.format(
            key.char))
    except AttributeError:
        print('按下特殊键{0}'.format(
            key))

def on_release(key):
    '''松开按键时执行'''

    print('{0} 释放'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# 收集按键时间直到结束
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

