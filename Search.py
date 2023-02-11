from CreateIndex import es
from getUrl import pageranks

def search(name):
    #短语查询：普通查询 V
    #站内查询：给定Url前缀 V
    #通配查询：es支持？V
    #查询日志：查询结果保存，游客一个，每个用户一个V
    #个性化查询：用户登录，根据不同用户保存查询日志，根据用户历史查询对搜索结果重排序
    #网⻚快照：用户查询结果保存到本地 V
    #个性化推荐：根据（全部）用户历史查询推荐相关查询词 每搜索一次都写到history kword，由此匹配 V
    #链接分析???
    print("欢迎使用南开大学资源搜索！")

    mode = ''
    history = open("history.txt", 'a')

    login = False
    usr = ''

    while(1):
        if login == False:
            print("登陆请输入0")
        print("普通查询请输入1（支持通配查询，*代表任意字符串、？代表任意字符）")
        print("站内查询请输入2")
        mode = input()
        while mode != '0' and mode != '1' and mode != '2':
            print("Bad Input, 请重新输入")
            mode = input()
        # 登陆
        if mode == '0':
            print("请输入用户名")
            usr = input()
            print("请输入密码")
            passwd = input()
            # Todo密码验证
            usrhistory = open(usr + '_' + "history.txt", 'a')
            login = True
            print("登陆成功！")

        if mode =='2':
            print("请输入要限定的站点域名：")
            url = input()
        print("输入要查询的内容:")
        kword = input()

        # 查询
        dsl = {
            'query': {
                'match': {
                    'text': kword
                }
            }
        }
        res = es.search(index=name, body=dsl)
        weblist={}
        print("\n查找到以下网页：")
        if mode == '2':
            for i in res['hits']['hits']:
                if url in i['_id']:
                    weblist[i['_id']] = i['_source']['title']
                    #print(i['_source']['title']+': '+i['_id'])
        else:
            for i in res['hits']['hits']:
                weblist[i['_id']] = i['_source']['title']
                #print(i['_source']['title']+': '+i['_id'])

        #PagePank Sort
        webPR={}
        for i in weblist.keys():
            if i in pageranks.keys():
                webPR[i]=pageranks[i]
            else:
                webPR[i]=0.00
        webPR = dict(sorted(webPR.items(), key=lambda x: x[1], reverse=True))
        for i in webPR.keys():
            #print(str(webPR[i])+weblist[i]+': '+i)
            print(weblist[i] + ': ' + i)


        # 日志存储
        history.write(kword + '\n')
        if login:
            usrhistory.write(kword + '\n')

        # 个性化推荐：
        history_word_distances={}
        readhis = open("history.txt", 'r')
        for i in set(readhis.read().split('\n')):
            if i == '':
                continue
            history_word_distances[i] = distance(i, kword)
        history_word_distances = sorted(history_word_distances.items(), key=lambda x: x[1])
        #print(history_word_distances)
        readhis.close()
        # 取前几个输出
        print("\n您可能还想查找：", end=' ')
        c = 0
        for i in history_word_distances:
            if i[1] != 0:
                c += 1
                if c >= 6:
                    print(i[0])
                    break
                else:
                    print(i[0], end='、')


        # 快照
        print("\n是否需要保存搜索结果快照？[Y/N]")
        ph = input()
        if ph == 'Y' or ph == 'y':
            if usr == '':
                print("请先登录")
                continue
            phfile = open(usr+" search for "+kword+".txt", 'w+')
            for i in weblist:
                phfile.write(weblist[i]+': '+i+'\n')
            print("保存成功，文件名："+phfile.name)
        elif ph != 'N' and ph != 'n':
            print("Bad Input")

        print("按任意键继续...")
        input()


def distance(string_a , string_b):
    m = len(string_a)
    n = len(string_b)
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    # 从空位置变到string_a每个位置的距离
    for col in range(m + 1):
        dp[0][col] = col
    # 从空位置变到string_b 每个位置的距离
    for row in range(n + 1):
        dp[row][0] = row

    # 填表
    for row in range(1, n+1):
        for col in range(1, m+1):
            if string_a[col-1] != string_b[row-1]:
                dp[row][col] = min(dp[row - 1][col], dp[row - 1][col-1], dp[row][col-1]) + 1
            else:
                dp[row][col] = dp[row-1][col-1]
    return(dp[n][m])
