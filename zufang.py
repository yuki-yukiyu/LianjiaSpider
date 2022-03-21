import requests
import threading
import pandas as pd
from lxml import etree
import itertools
from numpy import *
# 全部信息列表
count=list()
average=list()

#生成1-10页url
def url_creat():
    #基础url
    url = 'https://hf.lianjia.com/zufang/feixi/pg{}/'
    #生成前10页url列表
    links=[url.format(i) for i in range(1,85)]
    return links

#对url进行解析
def url_parse(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'lianjia_uuid=c84284d6-1544-45e2-9163-44ff8af80be6; sajssdk_2015_cross_new_user=1; _ga=GA1.2.1887844120.1647589589; _gid=GA1.2.2121091591.1647589589; UM_distinctid=17f9bfe2deb530-0c89b4dde57bad-133a645d-1d73c0-17f9bfe2decaca; _smt_uid=6234396b.3e9ef755; _jzqckmp=1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1647589602,1647593188; _jzqc=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217f9bfdf24a2ce-026b6c939bbe22-133a645d-1930176-17f9bfdf24b1408%22%2C%22%24device_id%22%3A%2217f9bfdf24a2ce-026b6c939bbe22-133a645d-1930176-17f9bfdf24b1408%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; select_city=340100; _qzjc=1; CNZZDATA1255633284=351013103-1647587912-%7C1647593060; GUARANTEE_POPUP_SHOW=true; GUARANTEE_BANNER_SHOW=true; _jzqa=1.208055950957456480.1647589740.1647595184.1647603332.4; _jzqx=1.1647589740.1647603332.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=hf%2Elianjia%2Ecom|jzqct=/ershoufang/feixi/; _qzja=1.495974480.1647593201813.1647595183640.1647603331938.1647595873158.1647603331938.0.0.0.11.3; _qzjto=11.3.0; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1647603332; CNZZDATA1254525948=1149381749-1647588947-%7C1647599747; CNZZDATA1255604082=1709269288-1647587920-%7C1647598720; lianjia_ssid=401fbc6f-5df7-4170-b11d-00b9fb3b6980; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMmMwZGZlOTBjY2RjNTEyYjI3ODU5MmQ2OTc3ZjI2YzEwMjMzOTQyYTMxNWU1YWZlOTA5ZjBlOTFmMTI3NTMyNTRkMzlmN2ZjOWFkYzc3ZDI3OTQzODQxYThlNzE5ZDIyN2VkNTYyYTZkNzQzNjFmODE1ZTA3Nzk0ODIwMWM0OWNjZDE3MDc1NjVmYjA0NDUyNWNmMjA5NGIwYTQzMjk4MWYzYzgyMTM0OWY4ZDY0MjcxNjU4YWQxOGIyZTg1ZDQ4MDgwNGI5ZDQ2Y2ExNzkzMmFiYWYzODVkN2MxNTg3MWMwN2I3NjcyMDVkMjc1MDQyY2NlYmE5MjIyNmZiMzU4ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI0OTA1ODkzMlwifSIsInIiOiJodHRwczovL2hmLmxpYW5qaWEuY29tL3p1ZmFuZy9mZWl4aS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
        'Host': 'hf.lianjia.com',
        'Pragma': 'no-cache',
        'Referer': 'https://hf.lianjia.com/zufang/feixi/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
    response=requests.get(url=url,headers=headers).text
    tree=etree.HTML(response)
    #ul列表下的全部li标签
    li_List=tree.xpath("//*[@class='content__list']/div")
    #创建线程锁对象
    lock = threading.RLock()
    #上锁
    lock.acquire()
    for li in li_List:
        #标题
        title=li.xpath('./div/p/a/text()')[0]
        title = title.replace(' ', '')
        title = title.replace('\n', '')
        #网址
        link= 'https://hf.lianjia.com' + li.xpath('./div/p/a/@href')[0]
        #位置
        postion=li.xpath('./div/p[2]/a/text()')[0]+li.xpath('./div/p[2]/a[2]/text()')[0]+li.xpath('./div/p[2]/a[3]/text()')[0]
        #朝向
        contents = li.xpath('./div/p[2]')[0].xpath('string(.)').strip()
        contents = contents.replace(' ', '')
        contents = contents.replace('\n', '')
        contents = contents.replace('精选/', '')
        orientation = contents.split('/')[2]
        #面积
        area=contents.split('/')[1]
        #厅室
        room=contents.split('/')[3]
        #租金
        total_price=li.xpath('./div/span/em/text()')[0] + '元/月'
        dic={'title':title,'position':postion,'orientation':orientation,'area':area,'room':room,'total_price':total_price,'link':link}
        # print(dic)
        #将房屋信息加入总列表中
        count.append(dic)
    #解锁
    lock.release()
def run():
    links = url_creat()
    thread_list = []
    #多线程爬取
    for i in links:
        x=threading.Thread(target=url_parse,args=(i,))
        thread_list.append(x)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    #将全部房屋信息转化为excel
    count.sort(key = lambda x:x["position"])
    print(len(count))
    for key, group in itertools.groupby(count, key=lambda x:x['position']):
        groupList = list(group)
        priceList = []
        priceList2 = []
        areaList = []
        for h in groupList:
            l = h['total_price'].replace('元/月','')
            a = h['area'].replace('㎡','')
            l = l.replace(',','')
            l = float(l)
            a = float(a)
            p = l/a
            priceList.append(l)
            priceList2.append(p)
            areaList.append(a)
        average_price = ("%.2f" % mean(priceList))
        average_area = ("%.2f" % mean(areaList))
        average_price2 = ("%.2f" % mean(priceList2))
        average.append({'position':key,'number':len(groupList),'average_total_price':average_price+'元/月', 'average_area':average_area+'㎡', 'average_price':average_price2+'元/月/平'})
    data1=pd.DataFrame(count)
    data2=pd.DataFrame(average)
    with pd.ExcelWriter('./houseInfo.xlsx') as writer:  
        data1.to_excel(writer, index=False, sheet_name='Sheet1')
        data2.to_excel(writer, index=False, sheet_name='Sheet2')
if __name__ == '__main__':
    run()
