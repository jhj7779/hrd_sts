import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import dload
from PIL import Image
from konlpy.tag import Komoran
from gtts import gTTS
import os
import time
import playsound #(1.2.2 verison)
import psutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

car = ['자동차정비','자동차']
archi1 = ['굴삭기','지게차','건설기계','건설기계운전']
archi2 = ['측량','지형공간정보','지형정보','공간정보']
accounting = ['회계','사무원','기초회계','전산세무','ERP','생산','물류','인사','회계']
computer = ['인공지능','빅데이터','개발자','ICT','정보보안','정보보호','스마트공장', '전산']
design = ['시각디자인','콘텐츠제작','디지털디자인','UI','UX','광고']
machine = ['CAD','CAM','카티아','MCT','밀링','기계설계','기계설계가공','기계설계제작','인벤터']
sun = ['태양광','전기내선']

temp = [['자동차정비','자동차'],
        ['굴삭기','지게차','건설기계','건설기계운전','건축'],
        ['측량','지형공간정보','지형정보','공간정보'],
        ['회계','사무원','기초회계','전산세무','ERP','생산','물류','인사','회계'],
        ['인공지능','빅데이터','개발자','ICT','정보보안','정보보호','스마트공장','컴퓨터', '전산'],
        ['디자인','시각디자인','콘텐츠제작','디지털디자인','UI','UX','광고'],
        ['기계','CAD','CAM','카티아','MCT','밀링','기계설계','기계설계가공','기계설계제작','인벤터'],
        ['전기','전자','태양광','전기내선']]

cpart = []
cname = []
cperiod = []

def ListCrawling() :
    url = "http://www.kb.or.kr/p/?j=23"
    htmlText = requests.get(url).text
    bsoup = BeautifulSoup(htmlText, "html.parser")
    btab = bsoup.find("table", {"class": "tbl-c tbl-fix"})
    btbody = btab.find('tbody').find_all('td')
    links = btab.find_all('a')

    count = 0
    lst = []
    link_lst = []

    for a in links:
        count += 1
        if count % 2 == 1:
            href = a.attrs['href']
            link_lst.append("http://kb.or.kr/" + href)

    for i in range(len(btbody)):
        if i % 2 == 1:
            lst.append(btbody[i].text.split('\n'))

    for i in range(len(lst)):
        cpart.append(lst[i][1])
        cname.append(lst[i][2])
        if '교육기간' in lst[i][3]:
            cperiod.append(lst[i][3])
        else:
            cperiod.append(lst[i][4])

def ImgCrawling() :
    url = "http://kb.or.kr"
    htmlText = requests.get(url).text
    bsoup = BeautifulSoup(htmlText, "html.parser")
    bdiv = bsoup.find("div", {"id": "j-contents"})
    img = bdiv.find_all('img')[1:]

    cnt = 0
    for i in img:
        if cnt == 8:
            break
        image = url + i.get("src")
        print(image)
        dload.save(image, f'imagesave/{cnt}.jpg')
        cnt = cnt + 1

def Speak(classname, startyear, startmonth, startday, i, count) :
    if count == 0:
        text = '개강 예정인 과정이 없습니다.'
    elif count == 1 :
        text = '곧 개강하는 과정은 '+ classname +'로, 개강일은 '+startyear+'년'+startmonth+'월'+startday+'일 입니다'
    else:
        text = '그 다음 개강하는 과정은 ' + classname + '로, 개강일은 ' + startyear + '년' + startmonth + '월' + startday + '일 입니다'
    tts = gTTS(text=text, lang='ko')
    filename = f'voice{i}.mp3'
    tts.save(filename)
    playsound.playsound(filename)

def FindClass(cpart, classname) :
    count = 1
    for andex, i in enumerate(cpart):
        if classname in i :
            a = cname[andex]
            b = cperiod[andex]
            print(a)
            print(b)
            Speak(a, b[7:11], b[12:14], b[15:17], andex, count)
            count = count + 1

def ViewImage():
    os.mkdir('C:/Users/KB/Documents/voice_recognition/imagesave')
    ImgCrawling()
    plt.imshow(mpimg.imread('C:/Users/KB/Documents/voice_recognition/imagesave/0.jpg'))
    plt.axis('off')
    plt.ion()
    plt.show()
    plt.pause(3)
    plt.close()
    for i in range(8):
        filename = f'C:/Users/KB/Documents/voice_recognition/imagesave/{i}.jpg'
        os.remove(filename)
    os.rmdir('C:/Users/KB/Documents/voice_recognition/imagesave')

def talk_list(temp_number):
    ListCrawling()
    if temp_number[0] == 0:
        classname = '자동차'
        FindClass(cpart, classname)
    elif temp_number[0] == 1 or temp_number[0] == 2:
        classname = '건축'
        FindClass(cpart, classname)
    elif temp_number[0] == 3:
        classname = '생산'
        FindClass(cpart, classname)
    elif temp_number[0] == 4:
        classname = '전산'
        FindClass(cpart, classname)
    elif temp_number[0] == 5:
        classname = '디자인'
        FindClass(cpart, classname)
    elif temp_number[0] == 6:
        classname = '기계'
        FindClass(cpart, classname)
    elif temp_number[0] == 7:
        classname = '전기'
        FindClass(cpart, classname)


r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    audio = r.listen(source)

a = r.recognize_google(audio, language='ko-kr')
text = a.replace(" ","")


# text = "기계 과정 알려줘"    # 마이크가 없을경우 주석해제

komoran = Komoran(userdic='user_dic.txt')
nouns = komoran.nouns(text)
pos = komoran.pos(text)


# print(nouns)
# print(pos)

for idx,item in enumerate(temp):
    for text in nouns:
        if text in item:
            temp_number = idx,text
            # print("개열번호:",temp_number)

for idx,i in enumerate(pos):
    if 'VV' in i[1]:
        TalkAndShow = pos[idx][0]
        # print(TalkAndShow)
        if TalkAndShow == '알리':
            talk_list(temp_number)
        elif TalkAndShow == '보이':
            ViewImage()

