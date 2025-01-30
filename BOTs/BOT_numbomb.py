from random import randint, choice
from sys import exit
import json
import time

# BOT_numbomb v20240713.0


def init():
    global nb_num,nb_min,nb_max
    nb_num = randint(1, 99)
    nb_min = 0
    nb_max = 100
    try:
        with open('./BOT_data/numbomb/config_nb.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        print(f'获取数字炸弹配置失败：{e}')
        time.sleep(1)
        exit()


def generate_punishment(config):
    try:
        with open(f'./BOT_data/numbomb/nb_punishments/{config["punishments"]}.json', 'r', encoding='utf-8') as punishments_file:
            punishments = json.load(punishments_file)
    except Exception as e:
        print(f'获取惩罚列表失败：{e}')
        time.sleep(1)
        exit()
    return f"给{choice(punishments['shei'])}发：“我{choice(punishments['dongci1'])}{choice(punishments['dongci2'])}{choice(punishments['binyu-dingyu'])}{choice(punishments['binyu'])}！”"


def get_answer(query,send,init_result,cache):
    rwiq = init_result['response_when_invalid_query']
    if not send:
        if query == '开始数字炸弹':
            print(f'1{send}')
            return '数字炸弹开始了喵！0~100。回复“结束数字炸弹”以结束游戏喵。', True, 'text', None
        else:
            print(f'2{send}')
            return '', False, 'text', None
    else:
        if query == '结束数字炸弹':
            print(f'3{send}')
            return '数字炸弹结束了喵。', False, 'text', None
        else:
            print(f'4{send}')
            pass
    try:
        input_num = int(query)
    except:
        return f'{rwiq}', send, 'text', None
    global nb_min,nb_max
    if nb_min < input_num < nb_max:
        if input_num > nb_num:
            nb_max = input_num
        elif input_num < nb_num:
            nb_min = input_num
        else:
            r = f'杂——鱼♥！炸弹{nb_num}爆炸了！为你自动生成的惩罚是：{generate_punishment(init_result)}游戏现已重启喵，0~100。'
            init()
            return r, send, 'text', None
    else:
        return f'{input_num}？', send, 'text', None
    percent = round(1 / len(range(nb_min,nb_max+1)[1:-1]) * 10000) / 100
    return f'{nb_min}~{nb_max}' + f'（下次爆炸概率：{percent}%）', send, 'text', None


