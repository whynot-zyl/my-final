import requests, random, re
import time
import os
import csv
import sys
import json
import importlib
from fake_useragent import UserAgent
from lxml import etree

importlib.reload(sys)
startTime = time.time()  # 记录起始时间

# --------------------------------------------文件存储-----------------------------------------------------
filename = 'comments.txt' #存储评论

# 设置heades
headers = {
    'Cookie': '_T_WM=22822641575; H5_wentry=H5; backURL=https%3A%2F%2Fm.weibo.cn%2F; ALF=1584226439; MLOGIN=1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5RJaVYrb.BEuOvUQ8Ca2OO5JpX5K-hUgL.FoqESh-7eKzpShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMceoBfeh2EeKBN; SCF=AnRSOFp6QbWzfH1BqL4HB8my8eWNC5C33KhDq4Ko43RUIzs6rjJC49kIvz5_RcOJV2pVAQKvK2UbAd1Uh6j0pyo.; SUB=_2A25zQaQBDeRhGeBM71cR8SzNzzuIHXVQzcxJrDV6PUJbktAKLXD-kW1NRPYJXhsrLRnku_WvhsXi81eY0FM2oTtt; SUHB=0mxU9Kb_Ce6s6S; SSOLoginState=1581634641; WEIBOCN_FROM=1110106030; XSRF-TOKEN=dc7c27; M_WEIBOCN_PARAMS=oid%3D4471980021481431%26luicode%3D20000061%26lfid%3D4471980021481431%26uicode%3D20000061%26fid%3D4471980021481431',
    'Referer': 'https://m.weibo.cn/detail/4312409864846621',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# -----------------------------------爬取战疫情首页的每个主题的ID------------------------------------------
comments_ID = []# 存储


def get_title_id():
    for page in range(1, 21):  # 每个页面大约有18个话题
        headers = {
            "User-Agent": UserAgent().chrome  # chrome浏览器随机代理
        }
        time.sleep(1)
        # 该链接通过抓包获得
        api_url = 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_600059_-_ctg1_600059&page=' + str(page)
        print(api_url)
        rep = requests.get(url=api_url, headers=headers)
        # 获取ID值并写入列表comment_ID中
        for json in rep.json()['data']['statuses']:
            comment_ID = json['id']
            comments_ID.append(comment_ID)


# -----------------------------------爬取战疫情每个主题的详情页面------------------------------------------
def spider_title(comment_ID):
    try:
        article_url = 'https://m.weibo.cn/detail/' + comment_ID
        #print("article_url = ", article_url)
        html_text = requests.get(url=article_url, headers=headers).text
        # 评论量
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        comment_count = int(int(comments_count) / 20)  # 每个ajax一次加载20条数据
        return comment_count
    except:
        pass


# -------------------------------------------------抓取评论信息---------------------------------------------------
# comment_ID话题编号
def get_page(comment_ID, max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    url = ' https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id'.format(comment_ID, comment_ID)
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)
        pass


# -------------------------------------------------抓取评论item最大值---------------------------------------------------
def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id


# -------------------------------------------------抓取评论信息---------------------------------------------------
def write_csv(jsondata):
    for json in jsondata['data']['data']:
        comments_text = json['text']
        comment_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', comments_text)  # 正则匹配掉html标签
        # 评论时间
        created_times = json['created_at'].split(' ')
        created_time = created_times[3]  # 评论时间时分秒
        with open(filename, 'a',encoding='utf-8') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(comment_text+'\n')


# -------------------------------------------------获取评论---------------------------------------------------
def  GetComment():
    count_title = len(comments_ID)
    for count, comment_ID in enumerate(comments_ID):
        # maxPage获取返回的最大评论数量
        maxPage = spider_title(comment_ID)
        m_id = 0
        id_type = 0
        if maxPage != 0:  # 小于20条评论的不需要循环
            try:
                # 用评论数量控制循环
                for page in range(0, maxPage):
                    # 自定义函数-抓取网页评论信息
                    jsondata = get_page(comment_ID, m_id, id_type)

                    # 自定义函数-写入CSV文件
                    write_csv(jsondata)

                    # 自定义函数-获取评论item最大值
                    results = parse_page(jsondata)
                    time.sleep(1)
                    m_id = results['max_id']
                    id_type = results['max_id_type']
            except:
                pass

# -------------------------------------------------获取疫情数据---------------------------------------------------

def GetCondition():
    path = os.getcwd() + "/virus.csv"
    csvfile = open(path, 'a', newline='', encoding = 'utf-8-sig')
    writer = csv.writer(csvfile)
    writer.writerow(("provinceName","cityName","province_confirmedCount","province_suspectedCount" ,"province_curedCount","province_deadCount", "city_confirmedCount", "city_suspectedCount","city_curedCount" ,"city_deadCount"))

    # 放入要爬的url
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    # 设置header做一个防爬机制
    header = {
        "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}
    # 获取response的json
    response = requests.get(url, headers=header)
    # 取得数据词典
    data = json.loads(response.content.decode())
    data_str = data['data']
    data_json = json.loads(data_str)
    # 取出各个省和市的dict
    areaTree = data_json['areaTree'][0]['children']
    # 更新时间
    lastUpdateTime = data_json['lastUpdateTime']
    for province_list in areaTree:
        province_name = province_list['name']
        confirm_total = province_list['total']['confirm']
        suspect_total = province_list['total']['suspect']
        dead_total = province_list['total']['dead']
        heal_total = province_list['total']['heal']
        for itemChild in province_list['children']:
            city_name = itemChild['name']
            confirm = itemChild['total']['confirm']
            suspect = itemChild['total']['suspect']
            dead = itemChild['total']['dead']
            heal = itemChild['total']['heal']
            # 插入数据
            writer.writerow((province_name,city_name,confirm_total,suspect_total,heal_total,dead_total,confirm,suspect,heal,dead))



def get():
    # 获取话题ID
    get_title_id()

    # 主操作
    GetComment()
    GetCondition()
    # 计算使用时间
    endTime = time.time()
    useTime = (endTime - startTime) / 60
    print("该次所获的信息一共使用%s分钟" % useTime)
