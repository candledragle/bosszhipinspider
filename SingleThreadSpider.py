# coding:utf-8

import requests
import json
import traceback

from queue import Queue
from threading import Thread

from lxml import etree
import re

import time

base_url = "https://www.zhipin.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

# 存储招聘信息的列表
jobs_queue = Queue()

# 创建存储url地址的队列
url_queue = Queue()

# 正则表达式：去掉标签中的<br/> 和 <em></em>标签，便于使用xpath解析提取文本
regx_obj = re.compile(r'<br/>|<(em).*?>.*?</\1>')

def send_request(url_path, headers, param=None):
    """
    :brief 发送请求，获取html响应(这里是get请求)
    :param url_path: url地址
    :param headers: 请求头参数
    :param param: 查询参数, 如：param = {'query': 'python', 'page': 1}

    :return: 返回响应内容
    """
    response = requests.get(url=url_path, params=param, headers=headers)

    response = regx_obj.sub('', response.text)

    return response

def detail_url(param):
    """
    :brief 获取详情页的url地址
    :param param:  get请求的查询参数
    :return: None
    """
    wuhan_url = '/'.join([base_url, "c101200100/h_101200100/"])

    html = send_request(wuhan_url, headers, param=param)
    # 列表页页面
    html_obj = etree.HTML(html)
    # 提取详情页url地址
    nodes = html_obj.xpath(".//div[@class='info-primary']//a/@href")
    for node in nodes:
        detail_url = '/'.join([base_url, node])  # 拼接成完整的url地址
        print(detail_url)
        url_queue.put(detail_url)  # 添加到队列中

def write_data(page):
    """
    :brief 将数据保存为json文件
    :param page: 页面数
    :return: None
    """
    with open('/home/sym/Documents/github/python-spider/wuhan_python_job_{}.json'.format(page), 'w', encoding='utf-8') as f:
        f.write('[')
        try:
            while True:
                job_dict = jobs_queue.get(timeout=25)
                job_json = json.dumps(job_dict, indent=4, ensure_ascii=False)
                f.write(job_json + ',')
        except:
            pass

        f.seek(0, 2)
        position = f.tell()
        f.seek(position - 1, 0)  # 剔除最后一个逗号
        f.write(']')


def detail_url(param):
    """
    :brief 获取详情页的url地址
    :param param:  get请求的查询参数
    :return: None
    """
    wuhan_url = '/'.join([base_url, "c101200100/h_101200100/"])

    html = send_request(wuhan_url, headers, param=param)
    # 列表页页面
    html_obj = etree.HTML(html)
    # 提取详情页url地址
    nodes = html_obj.xpath(".//div[@class='info-primary']//a/@href")
    for node in nodes:
        detail_url = '/'.join([base_url, node])  # 拼接成完整的url地址
        print(detail_url)
        url_queue.put(detail_url)  # 添加到队列中

def parse_data():
    """
    :brief 从html文本中提取指定信息
    :return: None
    """
    print("parse_data +++++++++++++++")
    # # 解析为HTML文档=

    try:
        print(" true  ============== true")
        # 等待25s，超时则抛出异常
        detail_url = url_queue.get(timeout=25)

        print("current : "+detail_url)

        html = send_request(detail_url, headers, param=None)
        # print html
        html_obj = etree.HTML(html)
        if len(html_obj):
            item = {}

            # 发布日期 //*[@id="main"]/div[3]/div/div[2]/div[1]/p/text()[2]
            xpaths = html_obj.xpath("//*[@id=\"main\"]/div[3]/div/div[2]/div[1]/p/text()")[0]
            # print (len(xpaths))
            # print (type(xpaths))
            # print (xpaths[0])
            print (xpaths)
            # 职位名
            item['position'] = html_obj.xpath(".//div[@class='info-primary']//h1/text()")[0]
            # # 发布者姓名
            # item['publisherName'] = html_obj.xpath("//div[@class='job-detail']//h2/text()")[0]
            # # 发布者职位
            # item['publisherPosition'] = html_obj.xpath("//div[@class='detail-op']//p/text()")[0]
            # # 薪水
            # item['salary'] = html_obj.xpath(".//div[@class='info-primary']//span[@class='badge']/text()")[0]
            # # 公司名称
            # item['companyName'] = html_obj.xpath("//div[@class='info-company']//h3/a/text()")[0]
            # # 公司类型
            # item['companyType'] = html_obj.xpath("//div[@class='info-company']//p//a/text()")[0]
            # # 公司规模
            # item['companySize'] = html_obj.xpath("//div[@class='info-company']//p/text()")[0]
            # # 工作职责
            # item['responsibility'] = html_obj.xpath("//div[@class='job-sec']//div[@class='text']/text()")[0].strip()
            # # 招聘要求
            # item['requirement'] = html_obj.xpath("//div[@class='job-banner']//div[@class='info-primary']//p/text()")[0]
            # print("ddd      : " + item)
            # jobs_queue.put(item)  # 添加到队列中
        time.sleep(1500)
    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':

    param = {'query': 'python', 'page': 1}
    detail_url(param)

    parse_data()
    write_data(1)
    pass