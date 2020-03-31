import requests
import re
import json
from lxml import etree
import time
import random
import collections
from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
def spider(user_url):
    response = requests.get(url,headers=headers)
    time.sleep(random.randint(4,7))
    pat = re.compile('</script><script id="js-initialData" type="text/json">(.*)</script><script src="https://static.zhihu.com/heifetz/vendor.7b36fae46082fd30a0db.js">')
    response_json = re.findall(pat,response.text)[0]
    user_following = list(json.loads(response_json).get('initialState')['entities']['users'].keys())[1:]
    next_urls = ['https://www.zhihu.com/people/' + username +'/following' for username in user_following]
    sel = etree.HTML(response.text)
    try:
        name = sel.xpath('//*[@class="ProfileHeader-name"]/text()')[0]
    except:
        name = '暂无数据'
    try:
        prefession = sel.xpath('//*[@class="ProfileHeader-infoItem"]/text()')[0]
    except:
        prefession = '暂无数据'
    try:
        following = sel.xpath('//*[@class="Card FollowshipCard"]/div/a[1]/div/strong/text()')[0]
    except:
        following = '0'
    try:
        follower = sel.xpath('//*[@class="Card FollowshipCard"]/div/a[2]/div/strong/text()')[0]
    except:
        follower = '0'
    print(name)
    collection.insert_one({'name':name,'prefession':prefession,'following':following,'follower':follower})
    return next_urls
need_crawl_urls = collections.deque()
need_crawl_urls.append('https://www.zhihu.com/people/gao-yuan-xiong-ying-1-69/following')
client = MongoClient()
db = client.zhihu2
collection = db.user
have_crawled_urls = set()
while True:
    url = need_crawl_urls.popleft()
    try:
        next_urls = spider(url)
        have_crawled_urls.add(url)
        pre_crawl_urls = set(next_urls) - have_crawled_urls
        need_crawl_urls.extend(pre_crawl_urls)
    except:
        pass
