import requests
import json
from time import sleep

# BOT_weather v1.0.0 for MOMOKO v2.2.0


def init():
    # 这是一个初始化函数，在程序开始时会被执行一次。你可以在这里初始化你的灵魂需要的全局变量。必选。
    try:
        with open('BOT_data/weather/config.json') as config_file:
            config = json.load(config_file)
        with open('BOT_data/weather/icons.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        dic = {}
        for line in lines:
            kv = line.split('-')
            dic[kv[0]] = kv[1].removesuffix('\n')
    except Exception as e:
        print('获取配置文件失败。')
        sleep(1)
        exit(1)
    return (config,dic)  # 这个函数的返回结果会被定义为全局变量BOT_init_result，并会被传入get_answer函数。


def get_answer(query, send, init_result, cache):
    # 这是最重要的函数，用来获取回复。你的灵魂中必须有这个函数。必选。
    # 传入函数的形参分别为：用户的消息、是否发送、初始化结果、配置文件。
    if not '天气' in query or query[-1] != '气':
        return "", False, 'text', None
    key = init_result[0]['key']
    icons = init_result[1]
    try:
        geo_info = requests.get(f'https://geoapi.qweather.com/v2/city/lookup?location={query.removesuffix("天气")}&key={key}&number=1&lang=zh').json()
        location_id = geo_info['location'][0]['id']
        location_name = geo_info['location'][0]['name']+' - '+geo_info['location'][0]['adm1']
    except Exception as e:
        try:
            if geo_info['code'] == '404':
                return '找不到对应的城市。',True,'text', None
        except Exception:
            return f'获取城市信息时发生错误：{e}',True,'text', None
    try:
        now = requests.get(f'https://devapi.qweather.com/v7/weather/now?location={location_id}&key={key}&lang=zh').json()['now']
        forecast = requests.get(f'https://devapi.qweather.com/v7/weather/24h?location={location_id}&key={key}&lang=zh').json()['hourly']
        warnings = requests.get(f'https://devapi.qweather.com/v7/warning/now?location={location_id}&key={key}&lang=zh').json()['warning']
    except Exception as e:
        return f'获取天气信息时发生错误：{e}',True,'text', None
    response = f'{location_name}：\n{icons[now["icon"]]} {now["text"]} {now["temp"]}℃\n{now["windDir"]+" "+now["windScale"]}级 | 相对湿度 {now["humidity"]}% | 小时累计降水 {now["precip"]}mm | 气压 {now["pressure"]}hPa | 能见度 {now["vis"]}km\n\n'
    for hour in forecast[0:6]:
        response += f'{hour["fxTime"].split("T")[1].split("+")[0].split("-")[0]} {icons[hour["icon"]]} {hour["text"]} {hour["temp"]}℃\n'
    if warnings:
        response += '\n'
    for warning in warnings:
        if not warning['severityColor']:
            warning['severityColor'] = 'Warning'
        response += f'{icons[warning["severityColor"]]} {warning["title"]}：{warning["text"]}\n'
    response += '\n（数据来源：和风天气。本条消息在CC BY-SA 4.0许可协议下提供）'
    response_type = 'text'
    send = True
    return response, send, response_type, None
