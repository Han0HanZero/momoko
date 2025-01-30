import uiautomation
import time
import json
from sys import exit
from uiautomation import Bitmap
import os
import logging

from BOTs import *

# MOMOKO
# Made by HanZero
# Thanks to https://space.bilibili.com/32828171
# v2.3.1
# 这个版本的桃桃子兼容v1.1.0版本的灵魂。
# This work is licensed under GPL-3.0 License.


with open('latest.log','w'):  # 创建日志文件
    pass
logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.INFO)


def report_err(errmsg:str) -> None:
    """报错函数。"""
    logging.critical(errmsg)
    input('程序已终止，按Enter以退出...')
    exit(1)


try:  # 获取配置
    with open('./config_ui.json','r',encoding='utf-8') as config_file:
        config = json.load(config_file)
except Exception as e:
    report_err(f'获取配置失败：{e}')

try:  # 设定配置
    BOT = globals()[config['BOT']]  # 指定要使用的灵魂
    window_name = config['windowName']  # 指定窗口名称
    uiautomation.SetGlobalSearchTimeout(config['timeOut'])  # 设定捕获窗口超时时间
except Exception as e:
    report_err(f'设定配置失败，请检查拼写。错误信息：{e}')

window = uiautomation.WindowControl(searchDepth=1, Name=window_name)  # 指定要捕获的窗口对象


def get_msg():
    """从微信窗口获取最新消息。"""
    msg_list = []
    try:
        msg_ctrl_list = window.ListControl().GetChildren()
    except Exception as e:
        report_err(f'获取消息控件列表失败，这可能是因为未找到窗口。{e}')
    for msg_ctrl in msg_ctrl_list:
        msg_list.append(msg_ctrl.Name)
    try:
        return msg_list[-1]  # 返回最新消息
    except:
        return ''


def send_respond(msg:str,msgtype:str):
    """向微信窗口发送消息。msgtype应当为text或img，若为img，msg需传入图像路径。"""
    window.SetActive()
    if msgtype == 'text':
        uiautomation.SetClipboardText(msg)
    elif msgtype == 'img':
        uiautomation.SetClipboardBitmap(Bitmap.FromFile(msg))
    window.SendKeys('{Ctrl}v')
    window.SendKey(13)


try:  # 初始化灵魂
    BOT_init_result = BOT.init()
    is_sends = False
except NameError as e:
    report_err(f'未找到灵魂。错误信息：{e}')
except Exception as e:
    report_err(f'初始化灵魂时发生错误。错误信息：{e}')
former_msg = get_msg()  # 定义最后一条新消息
latest_respond = ''  # 定义最后一条响应
is_sends = [False]  # 初始化是否发送列表
is_send = False  # 初始化是否发送
cache = None
logging.info('窗口捕获成功，已开始运行')
print('----------\n窗口捕获成功，已开始运行\n----------')
while True:  # 主循环
    latest_msg = get_msg()  # 获取最后一条消息
    if latest_msg != former_msg:  # 判断最后一条消息是否为新消息
        if latest_msg != latest_respond:  # 判断最后一条消息是否是最后一条响应，如果不是，则进入新消息处理流程
            logging.info('【收到消息】' + latest_msg + ' - ' + time.ctime())
            print('【收到消息】' + latest_msg + ' - ' + time.ctime())
            former_msg = latest_msg  # 定义最后一条新消息为最后一条消息
            if '切换BOT' in latest_msg:  # 如果是切换灵魂命令
                old_BOT = BOT
                try:
                    BOT = globals()[latest_msg.replace('切换', '')]
                    BOT_init_result = BOT.init()
                    is_sends = False
                except KeyError as e:
                    responds = f'未找到灵魂。错误信息：{e}'
                    logging.error(responds)
                    BOT = old_BOT
                except Exception as e:
                    responds = f'灵魂初始化失败。错误信息：{e}'
                    logging.error(responds)
                    BOT = old_BOT
                else:
                    responds = '灵魂切换成功。'
                    logging.info(responds)
                is_sends = True
                old_BOT = None
                msgtypes = 'text'
            else:  # 如果不是切换灵魂命令
                try:
                    responds, is_sends, msgtypes, cache = BOT.get_answer(latest_msg, is_send, BOT_init_result, cache)  # 请求响应
                except Exception as e:
                    logging.error(f'尝试获取响应时发生错误：{e}')
                    responds, is_sends, msgtypes = f'尝试获取响应时发生错误：{e}', True, 'text'
            if type(responds) == str and type(is_sends) == bool and type(msgtypes) == str:  # 检查响应是一个还是一组
                responds, is_sends, msgtypes = [responds], [is_sends], [msgtypes]
            for respond, is_send, msgtype in zip(responds, is_sends, msgtypes):  # 响应发送流程
                if len(respond) == 0:  # 判断是否有响应
                    logging.warning('桃桃子没有响应\n----------')
                    continue
                if not is_send:  # 判断是否发送
                    logging.info('is_send为假')
                    continue
                if msgtype == 'text': # 判断响应类型并设定最后响应
                    latest_respond = '【桃桃子】' + respond
                else:
                    latest_respond = respond
                send_respond(latest_respond,msgtype)  # 发送响应
                if respond == '灵魂切换成功。':  # 切换并发送提示后将是否发送设定为假
                    is_send = False
                if msgtype == 'img':  # 发送图片后设定最后响应为'[图片]'
                    latest_respond = '[图片]'
                logging.info(f'【发送回复】{latest_respond}')
                print(f'【发送回复】{latest_respond}' + ' - ' + time.ctime())
                print('----------')
                logging.info('正在尝试清除缓存')
                for file_name in os.listdir('./cache'):  # 清除缓存
                    file_path = os.path.join('./cache', file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
