import requests
import re
import json
from lxml import etree
import time
import random
import collections
from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
def spider(user_url):
    response = requests.get(user_url,headers=headers)#发起请求
    time.sleep(random.randint(3,7))
    pat = re.compile('<script id="js-initialData" type="text/json">(.*)</script><script src="https://static.zhihu.com/heifetz/vendor.7e94b6f1bbc8e94cdcd4.js">')#建立pat提取内容
    response_json = re.findall(pat, response.text)[0]#提取json数据
    user_following = list(json.loads(response_json).get('initialState')['entities']['users'].keys())[1:]
    next_urls = ['https://www.zhihu.com/people/' + username + '/following' for username in user_following]
    sel = etree.HTML(response.text)
    username = sel.xpath('//*[@class="ProfileHeader-name"]/text()')[0]
    try:
        prefession = sel.xpath('//*[@class="ProfileHeader-infoItem"]/text()')[0]
    except:
        prefession = ''
    try:
        followings = sel.xpath('//*[@class="Card FollowshipCard"]/div/a[1]/div/strong/text()')[0]
    except:
        followings = 0
    try:
        followers = sel.xpath('//*[@class="Card FollowshipCard"]/div/a[2]/div/strong/text()')[0]
    except:
        followers = 0
    print(username)
    collection.insert_one({'name': username,'prefession':prefession,'followings':followings,'followers':followers})
    return next_urls
need_crawl_urls = collections.deque()
need_crawl_urls.append('https://www.zhihu.com/people/gao-yuan-xiong-ying-1-69/following')
client = MongoClient()
db = client.zhihu
collection = db.users
have_crawl_urls = set()
while True:
    url = need_crawl_urls.popleft()
    try:
        next_urls = spider(url)
        have_crawl_urls.add(url)
        pre_crawl_urls = set(next_urls) - have_crawl_urls
        need_crawl_urls.extend(pre_crawl_urls)
    except:
        pass
