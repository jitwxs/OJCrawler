import requests,re,json,os
from bs4 import BeautifulSoup

zojHost = 'http://acm.zju.edu.cn'
baseLoc = os.getcwd()
name = 'ZOJ'

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
    soup = getSoupObj(url)
    content = soup('div',{'id':'content_body'})
    if len(content) != 0:
        title = content[0].find_all('span',{'class':'bigProblemTitle'})[0]
        timeLimit = 
        memoryLimit = 
        print(content)
##    title = soup('h1')[0].text
##    problemInfo = soup('div',{'class':'rfloat','id':'problemInfo'})
##    problemContent = soup('div',{'id':'problemContent'})
##    if len(problemInfo) != 0:
##        timeLimit = problemInfo[0].find_all('div',{'class':'limit'})[0].find_all('div',{'class':'value'})[0].text
##        memoryLimit = problemInfo[0].find_all('div',{'class':'limit'})[1].find_all('div',{'class':'value'})[0].text
##        codeLimit = problemInfo[0].find_all('div',{'class':'limit'})[2].find_all('div',{'class':'value'})[0].text
##    if len(problemContent) != 0:
##        problemContext = problemContent[0].text
##    problemLoc = os.getcwd()+'//'+title + '.txt'
##    print('正在存储题目：'+ title + '\n')
##    with open(problemLoc, 'w') as f:
##        f.write('标题:\n\n'+title)
##        f.write('\n时间限制：\n'+timeLimit)
##        f.write('内存限制：\n'+memoryLimit)
##        f.write('代码长度限制：\n'+codeLimit)
##        f.write('\n问题内容：\n'+problemContext)

def getInfo(url):
    global baseLoc,zojHost,name
    soup = getSoupObj(url)
    zojLoc = baseLoc + '\\' + name
    if not os.path.exists(baseLoc + '\\' + name):
        os.mkdir(name)
        print('开始爬取: ' + name)
    os.chdir(zojLoc)
    examDict = getExamDict(url)
    for examKey,examValue in examDict.items():
        os.chdir(zojLoc)
        if not os.path.exists(zojLoc + '\\' + examKey):
            os.mkdir(examKey)
            print('开始爬取题目集: ' + examKey + '\n')
        examLoc = zojLoc + '\\' + examKey
        os.chdir(examLoc)
        problemList = getProblemList(zojHost + examValue)
        for problemValue in problemList:
            parsePromblem(zojHost + problemValue)

if __name__=="__main__":
    contestUrl = zojHost + '/onlinejudge/showContests.do'
##    print('************ZOJ竞赛题目爬虫************')
##    input('按Enter键开始爬取')
##    getInfo(contestUrl)
    parsePromblem(zojHost + '/onlinejudge/showContestProblem.do?problemId=5577')
