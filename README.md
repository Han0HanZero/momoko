# 桃桃子
English: https://github.com/Han0HanZero/momoko/blob/main/README_en.md
## 简介
桃桃子是一个基于uiautomation库的微信机器人，能够监听微信电脑版v3的消息窗口的信息，进行处理，并发送回复。回复支持纯文本和图片。

建议使用Python 3.11。

最新版本可能不会在GitHub同步更新。
## 特性
- 可定制的功能（被称为灵魂/BOT）。
- 屎山代码。
## 内置灵魂
斜体表示当前版本下可用性未经验证，删除表示暂不可用。
- _animalchess_：一个4x4斗兽棋。
- _debug_：一个debug用的灵魂。
- deepseek：一个可用于与DeepSeek API通信的灵魂。
- _dian_：一个用于获取一句名言的灵魂。
- _geteropics_：一个可从一个API获取二次元图片的灵魂。
- _kaizifu_：一个可用于游玩开字符游戏的灵魂，类似于音游的开字母游戏。
- _numbomb_：一个数字炸弹。
- _weather_：一个从和风天气API获取天气实况和预报的灵魂。
- _websearch_：一个百度搜索灵魂。
- ~~wechat_ai~~：一个可用于与微信对话API通信的灵魂。
## 使用方法
1. 打开微信电脑版，打开任意一个聊天窗口。
2. 将该窗口标题填入config_ui.json中的“window_name”中。
3. 在“BOT”中填写任意一个BOT的名字，例如：“BOT_deepseek”。
4. 运行WAY_uiautomation.py。如果出现“窗口捕获成功”，则表示启动成功。在聊天中发送“切换BOT_xxx”可切换灵魂。
## 已知bug(s)
- 当回复的文本中带有Emoji时，文本的最后一个或几个字符会消失。
- 不兼容微信电脑版v4。
## 兼容性
- 已经验证兼容Windows 11。其它系统的兼容性未经验证。
## 本地化
- 简体中文。