# MOMOKO
简体中文：https://github.com/Han0HanZero/momoko/README.md
## Introduction
MOMOKO is a WeChat/Weixin bot based on uiautomation. She is able to monitor the messages in the chat window of WeChat/Weixin (PC Edition), process them, and send a reply, which can be a text or a photo.

Python 3.11 is recommended.

The latest version might not be uploaded to GitHub in time.
## Functions
- Customizable functions (called _BOT_).
- Spaghetti code.
## Built-in BOTs
_Italic_ indicates that the availability of this version has not been verified yet, while ~~spaghetti~~ indicates that this BOT is unavailable for now.
- _animalchess_: A 4x4 animal chess.
- _debug_: A BOT for debugging.
- deepseek: A BOT that could communicate with DeepSeek API.
- _dian_: A BOT designed to get a saying.
- _geteropics_: A BOT designed to get anime pictures from an API.
- _kaizifu_: A BOT designed to play Kaizifu, which is like Kaizimu in some rhythm game groups.
- _numbomb_: A number bomb game.
- _weather_: A BOT designed to get weather (now & forecast) from QWeather API.
- _websearch_: A BOT for searching on Baidu.
- ~~wechat_ai~~: A BOT that could contact with a chat API developed by Weixin.
## How to use
1. Open Weixin/WeChat PC Edition, then open a chat.
2. Fill the "window_name" of config_ui.json with the title of the window.
3. Fill the "BOT" with the name of a BOT, e.g."BOT_deepseek".
4. Run WAY_uiautomation.py. A text of "窗口捕获成功" should appear. Use "切换BOT_xxx" to change a BOT.
## Known bug(s)
- A response containing emoji(s) loses its last character(s).
- Incompatible with Weixin PC Edition v4
## Compatibility
- Verified on Windows 11. Compatibility with other OS is unverified.
## Localization
- Simplified Chinese.