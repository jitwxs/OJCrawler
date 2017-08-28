import requests,re,json,os
from bs4 import BeautifulSoup

HOST = 'http://poj.org/'
BASELOC = os.getcwd()
NAME = 'POJProblems'

def getHTMLText(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        r = requests.get(url,timeout=30,headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def getSoupObj(url):
    try:
        html = getHTMLText(url)
        soup = BeautifulSoup(html,'html.parser')
        return soup
    except:
        print('\nError: failed to get the Soup object')
        return None

def getProblemList(url):
    soup = getSoupObj(url)
    list = []
    tmps = soup('a',{'href':re.compile(r'problem\?id=[\d]*')})
    for i in tmps:
        list.append(i.attrs['href'])
    return list

def parsePromblem(url):
    pid = url[url.find('=')+1:]
    soup = getSoupObj(url)
    title = soup('title')[0].text
    tr = re.compile(r'[<>,/,\,|,:,"",*,?]')
    title = tr.sub('',title)
    problemLoc = os.getcwd()+'\\'+ title + '.txt'

    tmps = soup('table',{'background':'images/table_back.jpg'})
    if len(tmps) != 0:
        data = tmps[0].find_all(['p','div','pre'])
        print('正在存储题目：'+ title + '\n')
        with open(problemLoc, 'w',encoding='utf-8') as f:
            f.write('Link: '+url+'\n\n')
            for i in data:
                f.write(i.text +'\n\n')

def getInfo(url):
    global BASELOC,HOST,NAME
    pojLoc = BASELOC + '\\' + NAME
    if not os.path.exists(BASELOC + '\\' + NAME):
        os.mkdir(NAME)
        print('开始爬取: ' + NAME)
    os.chdir(pojLoc)
    soup = getSoupObj(url)
    links = soup('a',{'href':re.compile(r'\?volume=[\d]*')})
    pageList = []
    for i in links:
        pageList.append(i.attrs['href'])
    pageList = sorted(set(pageList),key=pageList.index)
    for i in pageList:
        problemList = getProblemList(HOST + i)
        for problemUrl in problemList:
            parsePromblem(HOST + problemUrl)

if __name__=="__main__":
    requestUrl = HOST + 'problemlist'
    print('************POJ题库题目爬虫************')
    input('按Enter键开始爬取')
    getInfo(requestUrl)
