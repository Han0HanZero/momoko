import requests
import time
import os

# BOT_geteropics v20240713.0


def init():
    if not os.path.exists('./BOT_data/geteropics/cache'):
        os.mkdir('./BOT_data/geteropics/cache')


def get_signature(token,userid):
    pass


def get_config():
    pass


def get_answer(query,send,init_result, cache):
    headers = {
        'Referer': 'https://www.weibo.com/'
    }
    filename = str(round(time.time() * 100))  # 文件名

    responses = requests.get(f"https://iw233.cn/api.php?sort=random&num=1&type=json")  # 获取json
    try:
        responses.raise_for_status()
    except:
        return f'连接到API服务器时出现问题，HTTP状态码为{str(responses.status_code)}。（404表示内容不存在，502表示服务器宕机，403表示你的连接被拒绝了）', None

    response = responses.json()
    pic_list = response['pic']

    for pic_url in pic_list:
        response_pic = requests.get(pic_url, headers=headers)  # 请求图片本体

        try:
            response_pic.raise_for_status()
        except:
            return f'连接到图片服务器时出现问题，HTTP状态码为{str(response_pic.status_code)}。（404表示内容不存在，502表示服务器宕机，403表示你的连接被拒绝了）', None

        pic_filename = pic_url.split('/')[-1]  # 获取图片文件名
        pic_format = pic_filename.split('.')[-1]  # 获取图片格式
        final_filename = f'{filename}.{pic_format}'  # 生成最终文件名 文件名_索引.格式
        with open(f'./BOT_data/geteropics/cache/{final_filename}', 'wb') as output:  # 写入文件
            output.write(response_pic.content)
        return f'./BOT_data/geteropics/cache/{final_filename}', True, 'img', None
