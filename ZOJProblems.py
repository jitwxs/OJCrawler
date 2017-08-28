import requests,re,json,os
from bs4 import BeautifulSoup

HOST = 'http://acm.zju.edu.cn'
BASELOC = os.getcwd()
NAME = 'ZOJProblems'

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
    hrefs = soup('td',{'class':'problemId'})
    list = []
    for i in hrefs:
        href = i.find_all('a')
        if len(href) != 0:
            list.append(href[0].attrs['href'])
    return list

def parsePromblem(url):
    pid = url[url.find('=')+1:]
    soup = getSoupObj(url)
    contents = soup('div',{'id':'content_body'})
    if len(contents) != 0 :
        title = contents[0].find_all('span',{'class':'bigProblemTitle'})[0].text
        dr = re.compile(r'<[^>]+>',re.S)
        text = dr.sub('',str(contents[0]))
        tr = re.compile(r'[<>,/,\,|,:,"",*,?]')
        title = pid +' ' + tr.sub('',title)
        problemLoc = os.getcwd()+'\\'+ title + '.txt'
        text = text[:text.find('Submit')].strip()
        print('正在存储题目：'+ title + '\n')
        with open(problemLoc, 'w',encoding='utf-8') as f:
            f.write('Link: '+url)
            f.write('\n\n')
            f.write(text)

def getInfo(url):
    global BASELOC,HOST,NAME
    zojLoc = BASELOC + '\\' + NAME
    if not os.path.exists(BASELOC + '\\' + NAME):
        os.mkdir(NAME)
        print('开始爬取: ' + NAME)
    os.chdir(zojLoc)
    soup = getSoupObj(url)
    links = soup('a',{'href':re.compile(r'pageNumber=[\d]*(\d)$')})
    linkList = []
    for i in links:
        linkList.append(i.attrs['href'])
    for link in linkList:
        problemList = getProblemList(HOST + link)
        for problemUrl in problemList:
            parsePromblem(HOST + problemUrl)

if __name__=="__main__":
    requestUrl = HOST + '/onlinejudge/showProblemsets.do'
    print('************ZOJ题库题目爬虫************')
    input('按Enter键开始爬取')
    getInfo(requestUrl)
