import requests
import re
from bs4 import BeautifulSoup


index = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
pingjiao_1 = 'http://eams.uestc.edu.cn/eams/evaluateStd!search.action'
pingjiao_2 = 'http://eams.uestc.edu.cn/eams/evaluateStd!loadQuestionnaire.action'
pingjiao_3 = 'http://eams.uestc.edu.cn/eams/evaluateStd!save.action'
pingjiao_4 = 'http://eams.uestc.edu.cn/eams/evaluateStd!lockResult.action'
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


def get_semester_id(u):
    url = 'http://eams.uestc.edu.cn/eams/evaluateStd.action'
    r = u.get(url)
    return r.headers['Set-Cookie'].split(';')[0].split('=')[1]


def ping(u, semester_id):
    data = {
        'semester.id': semester_id
    }
    result = u.post(pingjiao_1, data=data)
    soup = BeautifulSoup(result.text, 'html.parser')
    for tr in soup.findAll('table', {'class': 'gridtable'})[0].select('tr')[1:-2]:
        d = tr.select('a')[0].attrs['href'].split('doEvaluate')[1].replace('(\'', '').replace('\')', '').replace('\'', '').split(',')
        lession_id = d[1]
        teacher_id = d[2]
        data_1 = {
            'semester.id': '163',
            'evaluateState': d[0],
            'evaluateId': ','.join(d[1:])
        }
        rst = u.post(pingjiao_2, data=data_1)
        if '重复登录' in rst.text:
            rst = u.post(pingjiao_2, data=data_1)
        # print(rst.text)
        sp = BeautifulSoup(rst.text, 'html.parser')
        data_2 = dict()
        data_2['semester.id'] = semester_id
        data_2['teacherId'] = teacher_id
        data_2['lesson.id'] = lession_id
        data_2['teacher.ids'] = teacher_id
        name = sp.findAll('li', {'align': "right"})[0].text.split('教师姓名')[0]
        for t in sp.findAll('tbody', {'id': "evaluateTB"})[0].select('tr'):
            d = t.select('input')[0]
            data_2[d.attrs['name']] = d.attrs['value']
        u.post(pingjiao_3, data=data_2)
        print(name + '已评教')
    # 提交
    if '您已完成全部课程的评价，请提交，提交后将不能修改。' in u.post(pingjiao_4, data=data).text:
        print('评教完成')
    else:
        print('评教失败，重启脚本或进入信息门户评教 http://eams.uestc.edu.cn/eams/evaluateStd!search.action')


if __name__ == '__main__':
    s = login()
    semester_id = get_semester_id(s)
    ping(s, semester_id=semester_id)

