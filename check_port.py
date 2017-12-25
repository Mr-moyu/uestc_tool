import requests
import re
from bs4 import BeautifulSoup
import os

index = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'

xuanke = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id='
jiaowu = 'http://eams.uestc.edu.cn/eams/home!submenus.action?menu.id='
headers = {
    "Host": "idas.uestc.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Referer": "http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/"
}


def login():
    u = requests.session()
    u.cookies.clear()

    r = u.get(index, headers=headers)
    lt = re.findall('name="lt" value="(.*)"/>', r.text)[0]
    username = input('学号：')
    password = input('密码：')
    data = {
        "username": username,
        "password": password,
        "lt": lt,
        "dllt": "userNamePasswordLogin",
        "execution": "e1s1",
        "_eventId": "submit",
        "rmShown": "1"
    }

    # 点击登陆
    r = u.post(index, headers=headers, data=data)
    r = u.get(jiaowu)
    if '重复登录' in r.text:
        st = re.findall("<a href=(.*)>", r.text)[0].split('"')[1]
        u.get(st)
    return u

if __name__ == '__main__':
    u = login()
    port = 0
    d = []
    with open('1.txt', 'wb') as f:
        while port < 4000:
            url = xuanke + str(port)
            r = u.get(url)
            if len(r.text) > 3000:
                d.append(port)
                f.write((str(port) + '               成功').encode('utf-8'))
                f.write('\r\n'.encode('utf-8'))
                print(str(port) + '               成功')
            elif len(r.text) > 2350:
                f.write((str(port) + '      未开放').encode('utf-8'))
                f.write('\r\n'.encode('utf-8'))
                print(str(port) + '      未开放', end='\r')
            else:
                print(str(port) + '  失败', end='\r')
            port = port + 1
    print(d)
