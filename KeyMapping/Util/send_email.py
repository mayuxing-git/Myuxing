import win32com.client as win32
import os

# 收件人邮箱列表
s_addres = 'MaYuXing@sogou-inc.com'
# 抄送人邮箱列表
cs_addres = '' + ';' + ''
# 获取要发送文件路径
file_path = os.path.join('D:\IDE\Project\KeyMapping','result_log','')

