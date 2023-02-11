import urllib.request
from bs4 import BeautifulSoup
import networkx as nx

g = nx.DiGraph()

urllist = dict()
pageranks=dict()
f=open("url.txt",'w+')
lab404=0
def getPageUrl(url):
    try:
        # 有仅内网访问的网页
        html = urllib.request.urlopen(url, timeout=1)
        html = html.read()
        html = html.decode("utf-8")
    except:
        urllist[url]=2
        return

    if g.has_node(url) is False:
        g.add_node(url)
    soup = BeautifulSoup(html, features='html.parser')
    tags = soup.find_all('a')
    count = 0
    for tag in tags:
        href = tag.get('href')
        if href is None or href == '':
            continue
        if (href[0] == '#'):  # 若是以"#"开头则不用处理
            continue
        if (href == "/" or href == "#" or "javascript:" in href):  ##若为图片等则跳过
            continue
        #print(href)

        if ("http" not in href):  # 若不包含http则拼接前缀
            if (href[0]=='/' and href[1]=='/'):
                href= "http:"+href
            elif (href[0]=='/'):
                href = url.split('/')[0] + '//' + url.split('/')[2] + href
            else:
                href = url.split('/')[0] + '//' + url.split('/')[2] +'/'+ href
        #print("##"+href)

        count+=1
        #print("##############################################")
        #print("text:", tag.get_text(), " href:", href)

        if (href not in urllist and "nankai.edu.cn" in href and '/c/' not in href):  # 如果当前链接已存在与list中，则已创建索引

            urllist[href] = 0
            f.write(href + '\n')

        if g.has_node(href) is False:
            g.add_node(href)
        if g.has_edge(url,href):
            g.add_edge(url, href)

    urllist[url] = 1


def getAllUrl(rootUrl, urllimit=500):
    # 图遍历算法？
    getPageUrl(rootUrl)

    urllist[rootUrl] = 1
    while( 0 in list(urllist.values())):
        for url in urllist:
            if urllist[url] == 2:
                break
            if urllist[url] == 0:
                getAllUrl(url)
            if len(urllist) >= urllimit:
                break
        if urllist[url] == 2:
            urllist.pop(url)
        if len(urllist) >= urllimit:
            break



def PagePank():
    print("总计获得Url数：" + str(len(urllist)))
    pageranks = nx.algorithms.link_analysis.pagerank(g)
    print(pageranks)
    #print(type(pageranks['https://www.nankai.edu.cn']))



