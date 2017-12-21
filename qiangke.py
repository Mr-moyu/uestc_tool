import requests
import re
from bs4 import BeautifulSoup
import os


# 登陆页面 data1 header
index = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'

# 教务系统
jiaowu = 'http://eams.uestc.edu.cn/eams/home!submenus.action?menu.id='

# 选课系统
xuanke = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id='


# 修改课程权重 data2
quanzhong = 'http://eams.uestc.edu.cn/eams/stdVirtualCashElect!changeVirtualCash.action'
data2 = {
    "lessonId": '277355',
    "changeCost": '13',
    "profileId": '998'
}
# 课表
kebiao2 = 'http://eams.uestc.edu.cn/eams/courseTableForStd.action?_=1497624774414'

# 所有课程 选课  port
all_course = 'http://eams.uestc.edu.cn/eams/stdElectCourse!queryStdCount.action?profileId='

# 单门课程 及人数 data3
course = 'http://eams.uestc.edu.cn/eams/stdVirtualCashElect!getLessonCost.action'
data3 = {
    'lessonId': '302688'
}

# 抢课 id:true:0  退课 id:false
qiangke = 'http://eams.uestc.edu.cn/eams/stdElectCourse!batchOperator.action?profileId='



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


def qiangKe(u, port, course_id, name, url_father=xuanke, url_children=qiangke):
    url1 = url_father + str(port)
    url2 = url_children + str(port)
    print(u.get(url1).status_code)
    data4 = {
        'operator0': str(course_id) + ':true:0'
    }
    r = u.post(url2, data=data4)
    print(r.status_code)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        s = soup.find(style="width:85%;color:green;text-align:left;margin:auto;")
        print(name + ':  ')
        if s is not None and '成功' in s.string:
            print('成功')
            print(s)
            return 1
        else:
            s = soup.find(style="width:85%;color:red;text-align:left;margin:auto;")
            print(s.string)
            return 0
    else:
        return -1


if __name__ == '__main__':
    u = login()
    portA = 1140  # check_port 或 自动分析
    portB = 1143
    while True:
        try:
            # a = qiangKe(u, portB, 302656, '植物鉴赏')
            # b = qiangKe(u, portB, 302246, '跨界创新')
            # c = qiangKe(u, portB, 302721, '中医基础理论与养生')
            # d = qiangKe(u, portB, 303462, '科学技术报告论文写作')
            # e = qiangKe(u, portB, 303152, '数学物理建模')

            # if d == -1:
            #     os.system('python3 qiangke.py')
            pass
        except Exception as e:
            # print(e)
            # os.system('python3 qiangke.py')
            pass




