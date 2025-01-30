import json
import requests
import time
from sys import exit
from os import path, mkdir

# BOT_deepseek v1.0.0-alpha
# 桃桃子灵魂格式v1.0.1，兼容主版本v2.3.1


def init():
    if not path.exists('./BOT_data/deepseek'):
        mkdir('./BOT_data/deepseek')
    try:
        with open('./BOT_data/deepseek/config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        print(f'获取配置失败：{e}')
        time.sleep(1)
        exit()


def get_answer(query: str, send: bool, init_result, cache=None) -> (str, bool, str):
    """这个函数用来处理消息、获取回复。必选。传入函数的形参分别为：用户的消息、是否发送、初始化结果、缓存。缓存会在下一次调用本函数时再次原封不动地被传入。"""
    if query.split(' ')[0] != '.ds':
        return '', False, 'text', None
    url = "https://api.deepseek.com/chat/completions"
    payload = json.dumps({
        "messages": [
            {
                "content": init_result['system_prompt'],
                "role": "system"
            },
            {
                "content": query.split(' ')[1],
                "role": "user"
            }
        ],
        "model": init_result['model'],
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {init_result["token"]}'
    }
    try:
        api_response = requests.post(url, headers=headers, data=payload)
        print(api_response.text)
        try:
            api_response.raise_for_status()
        except requests.HTTPError:
            response = f'请求时发生错误：{str(api_response.status_code)}'
        else:
            api_response = api_response.json()
            choice = api_response['choices'][0]
            finish_reason_dict = {
                'stop': '',
                'length': '——由于长度达到限制，输出被停止。\n',
                'content_filter': '——由于触发过滤策略，输出被停止。\n',
                'insufficient_system_resource': '——由于系统推理资源不足，输出被停止。\n'
            }
            finish_reason = finish_reason_dict[choice['finish_reason']]
            content = choice['message']['content']
            if init_result['model'] == 'deepseek-reasoner':
                reasoning_content = '('+choice['message']['reasoning_content']+')\n'
            else:
                reasoning_content = ''
            usage = api_response['usage']
            tokens = usage['total_tokens'] - usage['prompt_cache_hit_tokens']
            response = f'DeepSeek：{reasoning_content}{content}\n{finish_reason}消耗token(s)：{tokens}'
    except Exception as e:
        response = f'请求时发生错误：{e}'
    send = True
    response_type = 'text'
    cache = None
    return response, send, response_type, cache