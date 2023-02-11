from getUrl import getAllUrl, PagePank
from CreateIndex import create_index, es
from Search import search

getAllUrl(rootUrl="https://www.nankai.edu.cn", urllimit=500)
PagePank()
create_index("hw5")
search("hw5")


