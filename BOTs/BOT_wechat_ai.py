import requests
import time
from sys import exit

# BOT_wechat_ai 暂停使用

def init():
    pass


def look_for_token():
    try:
        with open('./token.txt','r') as token_file:
            return token_file.read()
    except Exception as e:
        print(f'获取token失败。{e}')
        time.sleep(1)
        exit()


def get_config():
    pass


def ask_for_query():
    query = input('你:')
    return query


def get_signature(token, userid):
    r = requests.post(f'https://chatbot.weixin.qq.com/openapi/sign/{token}', data = {'userid':userid})
    try:
        return r.json()['signature']
    except Exception as e:
        print(f'获取Signature失败，请检查token。{e}')
        time.sleep(1)
        exit()


def get_answer(token, signature, query, is_send, config):
    r = requests.post(f'https://chatbot.weixin.qq.com/openapi/aibot/{token}', data = {'signature':signature, 'query':query, "env":'online'})
    return r.json()['answer'], True, 'text'


'''
while True:
    query = ask_for_query()
    print('BOT:' + get_answer(get_signature(), query))
'''
