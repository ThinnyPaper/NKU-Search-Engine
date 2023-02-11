from getUrl import urllist, pageranks

from elasticsearch import Elasticsearch
from selenium import webdriver
import lxml.html as lh
import re


es = Elasticsearch()

def get_text(url = "https://www.nankai.edu.cn"):
    #driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
    except:
        print("Url open error")
        return '', ''
    html_source = driver.page_source
    #print(html_source)
    name = driver.title
    driver.quit()
    main_text = ""
    """获取文本"""
    if (html_source != ""):
        html = lh.fromstring(html_source)
        texts = html.xpath(
            "//p//text()|//h1//text()|//h2//text()|//h3//text()|//br//text()|//b//text()")
        pattern = re.compile("^\s+|\s+$|\n")
        # 获取本url页面文本
        for text in texts:
            line = re.sub(pattern, "", text)
            if (len(line) > 0):
                main_text += line.replace(" ", "")
    return name, name+main_text


def create_index(name):
    mapping = {
        'properties': {
            'title': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            },
            'text':{
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            },
            'PR': {
                'type': 'float',
            }
        }
    }
    if (es.indices.exists(index=name) is not True):
        es.indices.create(index=name)
        res = es.indices.put_mapping(index=name, body=mapping)
        print(res)
    else:
        print("index existed")

    for url in urllist.keys():
        if es.exists(index=name, id=url) is True:
            """
            itle, text = get_text(url)
            data = {
                "title": title,
                "text": text
            }
            es.update(index=name, id=url, body=data)
            """
            continue
        else:
            title, text = get_text(url)
            PR = 0.00
            if url in pageranks.keys():
                PR = pageranks[url]
            #print(PR)
            data = {
                "title": title,
                "text": text,
                "PR": PR
            }
            res = es.create(index=name, id=url, body=data)
    print("seccess")



#test("https://www.nankai.edu.cn")

"""    dsl = {
        'query': {
            'match': {
                'title': '南开'
            }
        }
    }
    es.search(index='hw4', body=dsl)"""
"""Elasticsearch security features have been automatically configured!
✅ Authentication is enabled and cluster connections are encrypted.

ℹ️  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  Hc-N9co0N_P_r+rYO5nb

ℹ️  HTTP CA certificate SHA-256 fingerprint:
  24ba6fb01a237201187be0d22abd8039812005dbfe0050c408ef3f4a7db66a26

ℹ️  Configure Kibana to use this cluster:
• Run Kibana and click the configuration link in the terminal when Kibana starts.
• Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjYuMCIsImFkciI6WyIxNzIuMTguMC4yOjkyMDAiXSwiZmdyIjoiMjRiYTZmYjAxYTIzNzIwMTE4N2JlMGQyMmFiZDgwMzk4MTIwMDVkYmZlMDA1MGM0MDhlZjNmNGE3ZGI2NmEyNiIsImtleSI6ImhmcVpNWVlCMFBrcjh6OVkxdVNpOkhnTno2b3F5UldHUTV3SGxsUTExUmcifQ==

ℹ️ Configure other nodes to join this cluster:
• Copy the following enrollment token and start new Elasticsearch nodes with `bin/elasticsearch --enrollment-token <token>` (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjYuMCIsImFkciI6WyIxNzIuMTguMC4yOjkyMDAiXSwiZmdyIjoiMjRiYTZmYjAxYTIzNzIwMTE4N2JlMGQyMmFiZDgwMzk4MTIwMDVkYmZlMDA1MGM0MDhlZjNmNGE3ZGI2NmEyNiIsImtleSI6Imh2cVpNWVlCMFBrcjh6OVkxdVNpOnRmeTJWWGU1VFRpaXFFWXpXQi1oNEEifQ==

  If you're running in Docker, copy the enrollment token and run:
  `docker run -e "ENROLLMENT_TOKEN=<token>" docker.elastic.co/elasticsearch/elasticsearch:8.6.0`
"""

