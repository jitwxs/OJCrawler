import requests,re,json,os
from bs4 import BeautifulSoup

HOST = 'http://acm.zju.edu.cn'
BASELOC = os.getcwd()
NAME = 'ZOJContests'

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

def getExamDict(url):
    soup = getSoupObj(url)
    tables = soup('table',{'class':'list'})
    if(len(tables) != 0):
        ass = tables[0].find_all('a')
        dict = {}
        for a in  ass:
            href = a.attrs['href']
            text = a.text
            dict[text] = href
    return dict

def getProblemList(url):   
    soup = getSoupObj(url)
    list = []
    problems = soup('td',{'class':'problemId'});
    for i in problems:
        a = i.find_all('a')
        if len(a) != 0:
            href = a[0].attrs['href']
            list.append(href)
    return list

def parsePromblem(url):
    pid = url[url.find('=')+1:]
    soup = getSoupObj(url)
    content = soup('div',{'id':'content_body'})
    if len(content) != 0:
        title = content[0].find_all('span',{'class':'bigProblemTitle'})[0].text
        dr = re.compile(r'<[^>]+>',re.S)
        text = dr.sub('',str(content[0]))
        tr = re.compile(r'[<>,/,\,|,:,"",*,?]')
        title = pid +' ' + tr.sub('',title)
        problemLoc = os.getcwd()+'\\'+ title + '.txt'
        text = text[:text.find('Submit')].strip()
        print('正在存储题目：'+ title + '\n')
        with open(problemLoc, 'w',encoding='utf-8') as f:
            f.write('Link: ' + url + '\n\n')
            f.write(text)

def getInfo(url):
    global BASELOC,HOST,NAME
    soup = getSoupObj(url)
    zojLoc = BASELOC + '\\' + NAME
    if not os.path.exists(BASELOC + '\\' + NAME):
        os.mkdir(NAME)
        print('开始爬取: ' + NAME)
    os.chdir(zojLoc)
    examDict = getExamDict(url)
    for examKey,examValue in examDict.items():
        os.chdir(zojLoc)
        if not os.path.exists(zojLoc + '\\' + examKey):
            os.mkdir(examKey)
            print('开始爬取题目集: ' + examKey + '\n')
        examLoc = zojLoc + '\\' + examKey
        os.chdir(examLoc)
        problemList = getProblemList(HOST + examValue)
        for problemValue in problemList:
            parsePromblem(HOST + problemValue)

if __name__=="__main__":
    requestUrl = HOST + '/onlinejudge/showContests.do'
    print('************ZOJ竞赛题目爬虫************')
    input('按Enter键开始爬取')
    getInfo(requestUrl)
