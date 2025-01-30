from random import randint
from time import sleep
import json

# BOT_kaizifu v20240713.0


def report_err(errmsg):
    print(errmsg)
    sleep(1)
    exit()


def init():
    # 这是一个初始化函数。你可以在这里初始化你的灵魂需要的变量。必选。
    global kzf_playing
    kzf_playing = False
    try:
        with open('./BOT_data/kaizifu/config_kzf.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        print(f'获取开字符配置失败：{e}')
        sleep(1)
        exit()


def generate_questions(config,number: int):  # 生成题目
    question_numbers = []
    question_list = []
    library = config['library']
    with open(f'./BOT_data/kaizifu/kzf_questions/{library}.txt','r',encoding='utf-8') as question_library:
        library_lines = question_library.readlines()
    for i in range(1,number+1):
        # question_numbers.append(randint(1,len(library_lines)))
        question_list.append(library_lines[randint(1,len(library_lines)) - 1].removesuffix('\n'))
    return question_list



def get_answer(query,send,init_result, cache):
    global kzf_playing, kzf_opened_list, kzf_question_list, kzf_correct_guesses
    response = ''
    final_response = ''
    if '开始开字符' in query:
        print('1')
        # kzf_playing = True
        kzf_opened_list = []
        kzf_correct_guesses = []
        try:
            number = int(query.split(' ')[1])
        except Exception as e:
            return f'获取题量失败。请检查。错误信息：{e}', True, 'text', None
        kzf_question_list = generate_questions(init_result, number)
        prefix = '开字符游戏现在开始了喵！请看以下题目：'
    elif not send:
        print('2')
        return '', False, 'text', None
    else:
        if '开 ' in query:
            character_open = query.removeprefix('开 ')
            print('3')
            if len(character_open) != 1:
                return '气死我啦！你这要开的根本不是1个字罢！（恼', True, 'text', None
            else:
                if character_open not in kzf_opened_list:
                    kzf_opened_list.append(character_open)
                    prefix = f'您开了“{character_open}”！'
                else:
                    return f'{character_open}已经被开过了欸……', True, 'text', None
        elif '猜 ' in query:
            print('4')
            try:
                question_number_guess = int(query.split(' ')[1])
            except ValueError:
                return '您格式错啦！应该是“猜 序号 题目”或“开 字符”。', True, 'text', None
            question_guess = query.removeprefix(f'猜 {str(question_number_guess)} ')
            if kzf_question_list[question_number_guess - 1] == question_guess:
                if question_number_guess not in kzf_correct_guesses:
                    kzf_correct_guesses.append(question_number_guess)
                    prefix = f'您猜对了！第{question_number_guess}个确实是{question_guess}呢~'
                    if len(kzf_correct_guesses) == len(kzf_question_list):
                        prefix = f'您猜对了！第{question_number_guess}个确实是{question_guess}呢~全部题目都被猜出来了！想要再来一局请输入”开始开字符 (数字)“喵！'
                else:
                    return f'{question_number_guess}已经被猜到了欸……', True, 'text', None
            else:
                return '您猜错了喵~', True, 'text', None
        else:
            print('5')
            return '', True, 'text', None
    for question in kzf_question_list:
        response += f'\n{kzf_question_list[int(kzf_question_list.index(question))]}'
    #print(kzf_opened_list)
    for character in response:
        if character in kzf_opened_list or character == '\n' or character == ' ':
            final_response += character
        else:
            final_response += '*'
    # 替换猜中的
    final_response = final_response.split('\n')
    del final_response[0]
    for correct_guess in kzf_correct_guesses:
        final_response[correct_guess-1] = kzf_question_list[correct_guess-1]
    true_final_response = ''
    for idk_what_to_name_here in final_response:
        true_final_response += f'\n{idk_what_to_name_here}'
    true_final_response = prefix + true_final_response
    return true_final_response, True, 'text', None



if __name__ == '__main__':
    with open('./BOT_data/kaizifu/config_kzf.json','r',encoding='utf-8') as config_file:
        config = json.load(config_file)
    generate_questions(config,5)
