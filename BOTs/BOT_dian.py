# 这是一个灵魂的模板。一个灵魂至少需要以下函数。
# BOT_example v1.0.0-alpha.3 for MOMOKO v2.2.0
import random


def init():
    # 这是一个初始化函数，在程序开始时和切换灵魂时会被执行一次。你可以在这里初始化你的灵魂需要的全局变量。必选。
    try:
        dian_list = []
        with open('./BOT_data/dian/dian.txt', 'r', encoding='utf-8') as dian_file:
            for sentence in dian_file:
                dian_list.append(sentence.removesuffix('\n').removeprefix('\n'))
            return dian_list
    except Exception as e:
        print(f'获取配置失败：{e}')
        exit()
    return None  # 这个函数的返回结果会被定义为全局变量BOT_init_result，并会被传入get_answer函数。


# get_signature() 已弃用。


# get_config() 已弃用。


def get_answer(query, send, init_result, cache):
    # 这是最重要的函数，用来获取回复。你的灵魂中必须有这个函数。必选。
    # 传入函数的形参分别为：用户的消息、是否发送、初始化结果。
    if '典' in query:
        response = init_result[random.randrange(0, len(init_result))]
        send = True  # 这是是否发送这条响应的指示器，是一个布尔值。
    else:
        response = ''
        send = False
    response_type = 'text'  # 这是你处理后响应信息的类型，目前只支持text和img
    return response, send, response_type, None
