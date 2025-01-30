# BOT_example v1.0.1
# 桃桃子灵魂格式v1.0.1，兼容主版本v2.3.1

# 这是一个灵魂的模板。一个灵魂至少需要以下函数。


def init():
    """这是一个初始化函数，在程序开始时和切换灵魂时会被执行一次。你可以在这里初始化你的灵魂需要的全局变量。必选。"""
    return None  # 这个函数的返回结果会被定义为全局变量BOT_init_result，并会被传入get_answer函数。


def get_answer(query: str, send: bool, init_result, cache=None) -> (str, bool, str):
    """这个函数用来处理消息、获取回复。必选。传入函数的形参分别为：用户的消息、是否发送、初始化结果、缓存。缓存会在下一次调用本函数时再次原封不动地被传入。"""
    response = ''  # 这是你处理后相应信息的内容。如果response_type是text，这应该是一个字符串。如果response_type是img，这应该是一个指向图片文件的路径字符串。不要在这里放None。
    send = True  # 这是是否发送这条响应的指示器，是一个布尔值。
    response_type = 'text'  # 这是你处理后响应信息的类型，目前只支持text和img
    cache = None
    if response_type == 'text' or response_type == 'img':
        pass
    else:
        response = '不支持的响应格式'
        send = False
        response_type = 'text'
    return response, send, response_type, cache
