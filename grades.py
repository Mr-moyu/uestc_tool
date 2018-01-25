import re
import time
import smtplib
import datetime
import requests
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
# testetstetssssss
index = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
pingjiao_1 = 'http://eams.uestc.edu.cn/eams/evaluateStd!search.action'
pingjiao_2 = 'http://eams.uestc.edu.cn/eams/evaluateStd!loadQuestionnaire.action'
pingjiao_3 = 'http://eams.uestc.edu.cn/eams/evaluateStd!save.action'
pingjiao_4 = 'http://eams.uestc.edu.cn/eams/evaluateStd!lockResult.action'
xuanke = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id='
jiaowu = 'http://eams.uestc.edu.cn/eams/home!submenus.action?menu.id='
grades = 'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=163&projectType='
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
    data = {
        "username": '学号',
        "password": '密码',
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


def get_grader(u, semesterid):
    data = {
        'semesterId': semesterid,
        'projectType': ''
    }
    r = u.post(grades, data=data, headers=headers)
    if '重复登录' in r.text:
        r = u.post(grades, data=data, headers=headers)
    return r.text


def prs_data(text):
    allSubject = []
    soup = BeautifulSoup(text, 'html.parser')
    _all = soup.findAll('tr')
    for index in _all[1:]:
        _list = index.findAll('td')
        subject = dict()
        subject['课程名'] = _list[3].string.strip()
        subject['学分'] = _list[5].string.strip()
        subject['成绩'] = _list[8].string.strip()
        subject['绩点'] = _list[9].string.strip()
        allSubject.append(subject)
    # _text = '''%-25s%-5s%-5s%-5s\r\n'''
    # Text = ''
    # for index in allSubject:
    #     Text += _text % (index['课程名'], index['学分'], index['成绩'], index['绩点'])
    # print(Text)
    _text = '''{:一^25}{:一^5}{:一^5}{:一^5}\r\n'''
    Text = _text.format('课程名', '学分', '成绩', '绩点')
    for index in allSubject:
        Text += _text.format(index['课程名'], index['学分'], index['成绩'], index['绩点'])
    print(Text)
    return Text, len(allSubject)


def to_email(Text):
    __user = '发送邮箱'
    __pwd = '授权码'
    __to = '接受邮箱（可以是自己）'

    msg = MIMEText(Text)
    msg['Subject'] = "hello good morning！"
    msg['From'] = __user
    msg['To'] = __to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(__user, __pwd)
        s.sendmail(__user, __to, msg.as_string())
        s.quit()
        print("Success!")
    except smtplib.SMTPException as e:
        print("Failed,%s" % e)


def main():
    u = login()
    id = get_semester_id(u)
    text = get_grader(u, id)
    Text, orgin = prs_data(text)
    to_email(Text)
    while True:
        u = login()
        id = get_semester_id(u)
        text = get_grader(u, id)
        Text, present = prs_data(text)
        if orgin != present:
            to_email(Text)
            orgin = present
        time.sleep(3600)

if __name__ == '__main__':
    main()
