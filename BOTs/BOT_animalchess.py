import json
import random
from PIL import Image


def judge_if_can_eat(current_unit, target_unit):  # 0：自己死了 1：同归于尽 2：吃了/移动了
    animals = ['ele', 'lio', 'tig', 'leo', 'wol', 'dog', 'cat', 'mou']
    if target_unit[0] is None:
        return 2
    if current_unit[0] == 'mou':
        if target_unit[0] == 'mou':
            return 1
        if target_unit[0] == 'ele':
            return 2
    if current_unit[0] == 'ele':
        if target_unit[0] == 'mou':
            return 0
        if target_unit[0] == 'ele':
            return 1
    if animals.index(current_unit[0]) < animals.index(target_unit[0]):
        return 2
    elif animals.index(current_unit[0]) == animals.index(target_unit[0]):
        return 1
    elif animals.index(current_unit[0]) > animals.index(target_unit[0]):
        return 0

def generate_board():
    animals = ['ele', 'lio', 'tig', 'leo', 'wol', 'dog', 'cat', 'mou']
    colors = ['red', 'blue']
    units = []
    for color in colors:
        for animal in animals:
            units.append([animal, color, False])  # 单位类型 颜色 是否翻开
    random.shuffle(units)
    board = {}
    for x in 'A B C D'.split():
        for y in '1 2 3 4'.split():
            board[x+y] = units.pop()
    return board


class AnimalGame:
    def __init__(self):
        self.board = generate_board()
        self.round = 1
        self.turn = random.choice(['red','blue'])
        with open('BOT_data/animalchess/config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            pack_name = config['pack']
        with open(f'BOT_data/animalchess/{pack_name}/names.json', 'r', encoding='utf-8') as pack_name_file:
            self.pack = json.load(pack_name_file)
        self.images = {}
        self.images['background'] = Image.open('BOT_data/animalchess/background.png').convert('RGBA')
        self.images['cover'] = Image.open('BOT_data/animalchess/cover.png').convert('RGBA').resize((173, 173))
        self.images['red_frame'] = Image.open('BOT_data/animalchess/red_frame.png').convert('RGBA').resize((173, 173))
        self.images['blue_frame'] = Image.open('BOT_data/animalchess/blue_frame.png').convert('RGBA').resize((173, 173))
        animals = ['ele', 'lio', 'tig', 'leo', 'wol', 'dog', 'cat', 'mou']
        for animal in animals:
            self.images[animal] = Image.open(f'BOT_data/animalchess/{pack_name}/{animal}.png').convert('RGBA').resize((173, 173))

    def flip(self, position):
        try:
            selected_unit = self.board[position]
        except KeyError:
            return False, '这个单位不存在。'
        if not selected_unit[0]:  # 检查是否为空
            return False, '这个位置上没有单位。'
        if selected_unit[2]:  # 检查翻开
            return False, '这个单位已经被翻开了。'
        self.board[position][2] = True
        self.round += 1
        self.turn = {'red': 'blue', 'blue': 'red'}[self.turn]
        return True, f'翻开了位于{position}的单位，它是{selected_unit[1]}方的{self.pack[selected_unit[0]]}！'

    def move(self, position, direction):
        x_dict = {'up':0,'down':0,'left':-1,'right':1}
        y_dict = {'up':-1,'down':1,'left':0,'right':0}
        try:
            selected_unit = self.board[position]
        except KeyError:
            return False, '这个单位不存在。'
        if not selected_unit[0]:  # 检查是否为空
            return False, '这个位置上没有单位。'
        if not selected_unit[2]:  # 检查翻开
            return False, '这个单位还没有被翻开，因此不能移动。'
        if selected_unit[1] != self.turn:  # 检查颜色
            return False, '你不能移动对方的单位。'
        current_x, current_y = list(position)
        target_x = 'A B C D'.split()['A B C D'.split().index(current_x)+x_dict[direction]]
        target_y = str(int(current_y)+y_dict[direction])
        target_position = target_x+target_y
        try:
            target_unit = self.board[target_position]
        except KeyError:
            return False, '目标单位不存在。'
        if not target_unit[2]:  # 检查翻开
            return False, '目标单位还没有被翻开，因此不能被吃掉。'
        if target_unit[1] == self.turn:  # 检查颜色
            return False, '你不能吃掉自己的单位。'
        if_can_eat = judge_if_can_eat(selected_unit, target_unit)
        if if_can_eat == 0: #自己被吃
            r = f'{self.turn}方的{self.pack[selected_unit[0]]}自杀了！'
            self.board[position] = [None, None, True]
            self.round += 1
            self.turn = {'red':'blue','blue':'red'}[self.turn]
            return True, r
        elif if_can_eat == 1: #都死
            r = f'{self.turn}方的{self.pack[selected_unit[0]]}与对方的{self.pack[target_unit[0]]}同归于尽了！'
            self.board[position] = [None, None, True]
            self.board[target_position] = [None, None, True]
            self.round += 1
            self.turn = {'red': 'blue', 'blue': 'red'}[self.turn]
            return True, r
        elif if_can_eat == 2:  # 吃了/移动了
            if target_unit[0] is None:
                r = f'{self.turn}方的{self.pack[selected_unit[0]]}向{direction}移动了一步。'
            else:
                r = f'{self.turn}方的{self.pack[selected_unit[0]]}吃掉了对方的{self.pack[target_unit[0]]}！'
            self.board[target_position] = self.board[position]
            self.board[position] = [None, None, True]
            self.round += 1
            self.turn = {'red': 'blue', 'blue': 'red'}[self.turn]
            return True, r
    def check_if_game_over(self):
        red_units = 0
        blue_units = 0
        blue_win = False
        red_win = False
        for unit in self.board.values():
            if unit[1] == 'red':
                red_units += 1
            if unit[1] == 'blue':
                blue_units += 1
        if red_units == 0:
            blue_win = True
        if blue_units == 0:
            red_win = True
        if red_win and blue_win:
            return True, '和棋'
        elif red_win:
            return True, '红方胜利'
        elif blue_win:
            return True, '蓝方胜利'
        else:
            return False, '游戏未结束'

    def generate_photo(self):
        background_copy = self.images['background'].copy()
        for position, unit in self.board.items():
            x = 138 + 'A B C D'.split().index(list(position)[0]) * 191
            y = 211 + (int(list(position)[1]) - 1) * 191
            if unit[0] is None:
                continue
            elif not unit[2]:
                background_copy.paste(self.images['cover'], (x,y), self.images['cover'])
            else:
                background_copy.paste(self.images[unit[0]], (x,y), self.images[unit[0]])
                background_copy.paste(self.images[unit[1]+'_frame'], (x, y), self.images[unit[1]+'_frame'])
        background_copy.save('BOT_data/animalchess/cache/cache.png')
        return 'BOT_data/animalchess/cache/cache.png'


def init():
    # 这是一个初始化函数，在程序开始时和切换灵魂时会被执行一次。你可以在这里初始化你的灵魂需要的全局变量。必选。
    global animal_chess_game
    animal_chess_game = None
    return None  # 这个函数的返回结果会被定义为全局变量BOT_init_result，并会被传入get_answer函数。


def get_answer(query, send, init_result, cache):
    # 这是最重要的函数，用来获取回复。你的灵魂中必须有这个函数。必选。
    # 传入函数的形参分别为：用户的消息、是否发送、初始化结果。
    global animal_chess_game
    color_emojis = {'red': '🔴', 'blue': '🔵'}
    if query == '开始斗兽棋':
        animal_chess_game = AnimalGame()
        response = [
            f'斗兽棋现已开始！本局游戏由{animal_chess_game.pack[animal_chess_game.turn]}先手。\n操作说明：使用“flip [位置]”来翻开一张卡牌，使用“move [位置] [up/down/left/right]”来移动一张卡牌。“位置”由一个大写字母和一个阿拉伯数字组成，且大写字母（横坐标）在前，不需添加逗号或分隔符。\n\n⭐ROUND {int(animal_chess_game.round)} ⭐\n{color_emojis[animal_chess_game.turn]}{animal_chess_game.pack[animal_chess_game.turn]}方的回合\n',
            animal_chess_game.generate_photo()]
        send = [True, True]
        response_type = ['text', 'img']
        return response, send, response_type, None
    elif query == '结束斗兽棋':
        animal_chess_game = None
        response = '斗兽棋已结束。'
        response_type = 'text'
        return response, False, response_type, None
    else:
        try:
            command = query.split(' ')
        except:
            return '', send, 'text', None
    if command[0] == 'flip':
        response = [animal_chess_game.flip(command[1])[1]+f'\n\n⭐ROUND {int(animal_chess_game.round)} ⭐\n{color_emojis[animal_chess_game.turn]}{animal_chess_game.pack[animal_chess_game.turn]}方的回合\n']
        response.append(animal_chess_game.generate_photo())
        send = [True, True]
        response_type = ['text', 'img']
    elif command[0] == 'move':
        response = [animal_chess_game.move(command[1], command[2])[1]+f'\n\n⭐ROUND {int(animal_chess_game.round)} ⭐\n{color_emojis[animal_chess_game.turn]}{animal_chess_game.pack[animal_chess_game.turn]}方的回合\n']
        response.append(animal_chess_game.generate_photo())
        game_over = animal_chess_game.check_if_game_over()
        send = [True, True]
        response_type = ['text', 'img']
        if game_over[0]:
            response.append('本局游戏结束，'+game_over[1]+'！使用“开始斗兽棋”可再玩一局。')
            animal_chess_game = None
            send.append(True)
            response_type.append('text')
    else:
        response = ''
        response_type = 'text'
    return response, send, response_type, None


if __name__ == '__main__':
    game = AnimalGame()
    game.generate_photo()
    print(game.board)
    print('ROUND'+str(game.round))
    print(game.turn+'的回合')
    while True:
        command = input('command...').split(' ')
        if command[0] == 'flip':
            print(game.flip(command[1])[1])
        if command[0] == 'move':
            print(game.move(command[1],command[2])[1])
        print(game.check_if_game_over())
        game.generate_photo()
        print(game.board)
        print('ROUND' + str(game.round))
        print(game.turn+'的回合')
