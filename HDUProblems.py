import requests,re,json,os
from bs4 import BeautifulSoup

HOST = 'http://acm.hdu.edu.cn/'
BASELOC = os.getcwd()
NAME = 'HDUProblems'

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
    tables = soup('table',{'class':'table_text'})
    list = []
    if len(tables) != 0:
        tmps = tables[0].find_all('script')
        if len(tmps) != 0:
            tmp = tmps[0].text
            tmp = tmps[0].text.split(';')
            for i in tmp:
                data = i.split(',')
                try:
                    list.append('showproblem.php?pid=' + data[1])
                except:
                    pass
    return list

def parsePromblem(url):
    pid = url[url.find('=')+1:]
    soup = getSoupObj(url)
    data = soup('div',{'class':re.compile(r'panel')})
    title = soup('h1')[0].text
    tr = re.compile(r'[<>,/,\,|,:,"",*,?]')
    title = pid +' ' + tr.sub('',title)
    problemLoc = os.getcwd()+'\\'+ title + '.txt'
    print('正在存储题目：'+ title + '\n')
    with open(problemLoc, 'w',encoding='utf-8') as f:
        f.write('Link: '+url+'\n\n')
        for i in data:
            f.write(i.text+'\n')

def getInfo(url):
    global BASELOC,HOST,NAME
    hduLoc = BASELOC + '\\' + NAME
    if not os.path.exists(BASELOC + '\\' + NAME):
        os.mkdir(NAME)
        print('开始爬取: ' + NAME)
    os.chdir(hduLoc)
    soup = getSoupObj(url)
    links = soup('a',{'href':re.compile(r'^(listproblem.php)')})
    linkDict = {}
    pageList = []
    for i in links:
        pageList.append(i.attrs['href'])
    pageList = sorted(set(pageList),key=pageList.index)
    for i in pageList:
        problemList = getProblemList(HOST + i)
        for problemUrl in problemList:
            parsePromblem(HOST + problemUrl)

if __name__=="__main__":
    requestUrl = HOST + 'listproblem.php'
    print('************HDU题库题目爬虫************')
    input('按Enter键开始爬取')
    getInfo(requestUrl)
