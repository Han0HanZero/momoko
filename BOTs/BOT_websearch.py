import requests
from bs4 import BeautifulSoup
import lxml

# BOT_websearch v20240712.0


def init():
    # 这是一个初始化函数。你可以在这里初始化你的灵魂需要的变量。非必选。
    pass
    return None # 这个函数不返回任何值


def get_config():
    pass

def get_answer(query,send,init_result,cache):
    params = {
        'wd': query,
        'cl': 3,
        'pn': 1,
        'ie':'utf-8',
        'rn':'10'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
        'cookie': 'BAIDUID=23891A85BA85C16E5C9B5560154BA69C:FG=1; BIDUPSID=B6A72EB557B74FFA3D56BB80DB603C2C; PSTM=1663062807; BD_UPN=13314752; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=alal2001850g8l81252h8aqu1hi0t9e18; ZFY=SEUInM0ZuRBXFZUw1B0dlkNP:BZj3M:BZlpxlcZfdCgw8:C; BD_HOME=1; H_PS_PSSID=36558_37117_37354_37300_36885_34812_36802_36789_37145_37258_26350_37364; delPer=0; BD_CK_SAM=1; PSINO=7; BDRCVFR[Fc9oatPmwxn]=aeXf-1x8UdYcs; BDUSS=Zpc0MwUDE5bTZ4dUdQcUIxM2Z1SnFZMEpvUGpxTlRBWTBaTjZVdlh1V0tDRWxqRVFBQUFBJCQAAAAAAQAAAAEAAACnhFosAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIp7IWOKeyFjUD; H_PS_645EC=18db%2FxuyDIkSXG5WHmpOcEYdpAWQjJ77VSAYXPxhCINzCpt3nIF4SZssA6n9ATbCjzGM; BDSVRTM=247; baikeVisitId=e2c826a7-6934-4751-ac3d-29e118347887'
    }
    response = requests.get('http://www.baidu.com/s',params=params,headers=headers)
    response.encoding='utf-8'
    #print(response.text)
    soup = BeautifulSoup(response.text,features='lxml')
    results = soup.find_all(class_='c-container')
    #results = soup.find_all(name='h3')
    print(results)
    print(f'共{len(results)}个结果')
    title_fail = 0
    link_fail = 0
    final_dict = {}
    for result in results:
        title = ''
        link = ''
        print(f'\n\n\n\n----------现在开始解析----------\n\n\n\n')
        print(result.prettify())
        print('\n\n\n\n------------------------------\n\n\n\n')
        try:
            title = result.div.h3.a.text
        except AttributeError as e:
            print(f'标题解析失败！正在跳过（{e}）')
            title_fail += 1
        try:
            link = result.a['href']
        except TypeError as e:
            print(f'链接解析失败！正在跳过（{e}）')
            link_fail += 1
        else:
            if not 'http' in link:
                print('链接解析失败！正在跳过（链接中没有http）')
                link_fail+=1
        print(f'\n-----\n标题：{title}\n链接：{link}\n-----\n')
        if title:
            final_dict[title] = link
    print(f'解析全部完成，标题解析失败{title_fail}，链接解析失败{link_fail}')
    for key in final_dict:
        print(key)
        print(final_dict[key])
    r = f'关键词“”的搜索结果如下：（共{len(results)}个结果，{len(results) - len(final_dict)}个结果解析失败）'
    for key in final_dict:
        r += f'\n{key}\n{final_dict[key]}'
    return r, send, 'text', None

if __name__ == '__main__':
    get_answer('','','橘子','','')

    # 记得加if https/https in判断防止百度视频链接解析失败
