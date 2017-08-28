import requests,re,json,os
from bs4 import BeautifulSoup

HOST = 'http://acm.nyist.net/JudgeOnline/'
BASELOC = os.getcwd()
NAME = 'NYOJProblems'

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
    problems = soup('td',{'class':'probname tal'});
    for i in problems:
        a = i.find_all('a')
        if len(a) != 0:
            href = a[0].attrs['href']
            list.append(href)
    return list

def parsePromblem(url):
    soup = getSoupObj(url)
    pid = url[url.find('=')+1:]
    title = soup('h2')[-1].text
    title = pid + ' ' + title
    limit = soup('div',{'class':'problem-ins'})[0].text
    content = soup('dl',{'class':'problem-display'})[0]
    if len(content) != 0:
        tmps = content.find_all(['dt','dd'])
        problemLoc = os.getcwd()+'\\'+ title + '.txt'
        print('正在存储题目：'+ title + '\n')
        with open(problemLoc, 'w',encoding='utf-8') as f:
            f.write('Link: ' + url + '\n\n')
            for i in tmps:
                f.write(i.text.strip()+'\n\n')

def getInfo(url):
    global BASELOC,HOST,NAME
    soup = getSoupObj(url)
    pages = soup('a',{'href':re.compile(r'page=[\d]*')})
    lastPageHref = pages[-1].attrs['href']
    lastPage = lastPageHref[lastPageHref.find('page=')+5:]
    nyojLoc = BASELOC + '\\' + NAME
    page = 1
    if not os.path.exists(BASELOC + '\\' + NAME):
        os.mkdir(NAME)
        print('开始爬取: ' + NAME)
    os.chdir(nyojLoc)
    while page <= int(lastPage):
        pageUrl = url + '?page=' + str(page)
        problemList = getProblemList(pageUrl)
        for problemValue in problemList:
            parsePromblem(HOST + problemValue)
        page += 1
    

if __name__=="__main__":
    requestUrl = HOST + 'problemset.php'
    print('************NYOJ题库题目爬虫************')
    input('按Enter键开始爬取')
    getInfo(requestUrl)
