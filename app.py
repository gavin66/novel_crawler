# -*- coding: UTF-8 -*-
import requests
from lxml import etree
from config import search as search_html
from config import chapters as chapters_html
from config import chapter as chapter_html
from urllib import parse as urlparse
import json

DEBUG = False


def search(keyword='绿茵峥嵘'):
    """
    小说搜索
    :param keyword:
    :return:
    """
    # print(keyword)
    html = ''
    if DEBUG is False:
        response = requests.get('http://www.b5200.net/modules/article/search.php', {'searchkey': keyword})
        if response.ok:
            html = response.text
    else:
        html = search_html

    root = etree.HTML(html)
    tr_list = root.xpath("//table[@class='grid']/tr")

    if isinstance(tr_list, list) is False:
        print('没有找到')

    result = []
    for tr_doc in tr_list:
        item = {
            'id': '',  # 图书 ID
            'name': '',
            'link': '',
            'recent': '',
            'recent_link': '',
            'author': '',
            'update': '',
            'recent_date': '',
            'status': '',
        }

        name_doc = tr_doc.xpath('./td[1]/a')
        link_doc = tr_doc.xpath('./td[1]/a/@href')
        recent_doc = tr_doc.xpath('./td[2]/a')
        recent_link_doc = tr_doc.xpath('./td[2]/a/@href')

        author_doc = tr_doc.xpath('./td[3]')
        update_doc = tr_doc.xpath('./td[5]')
        recent_date_doc = tr_doc.xpath('./td[6]')
        status_doc = tr_doc.xpath('./td[7]')

        if len(name_doc) > 0:
            item['name'] = name_doc[0].text
        else:
            continue
        if len(link_doc) > 0:
            item['link'] = urlparse.urlsplit(link_doc[0]).path
        if len(recent_doc) > 0:
            item['recent'] = recent_doc[0].text
        if len(recent_link_doc) > 0:
            item['recent_link'] = recent_link_doc[0]
        if len(author_doc) > 0:
            item['author'] = author_doc[0].text
        if len(update_doc) > 0:
            item['update'] = update_doc[0].text
        if len(recent_date_doc) > 0:
            item['recent_date'] = recent_date_doc[0].text
        if len(status_doc) > 0:
            item['status'] = status_doc[0].text

        result.append(item)

    return json.dumps(result, ensure_ascii=False)


def catalog(path='/97_97046/'):
    """
    小说的所有章节
    :return:
    """
    html = ''
    if DEBUG is False:
        response = requests.get('http://www.b5200.net/%s' % path)
        if response.ok:
            html = response.text
    else:
        html = chapters_html

    root = etree.HTML(html)
    dd_list = root.xpath("//div[@id='list']/dl/dd[position()>9]")

    if isinstance(dd_list, list) is False:
        print('没有找到')

    result = []
    for dd_doc in dd_list:
        item = {
            'name': '',
            'link': '',
        }
        name_doc = dd_doc.xpath('./a')
        link_doc = dd_doc.xpath('./a/@href')

        if len(name_doc) > 0:
            item['name'] = name_doc[0].text
        if len(link_doc) > 0:
            item['link'] = urlparse.urlsplit(link_doc[0]).path

        result.append(item)

    return json.dumps(result, ensure_ascii=False)


def chapter(path='/97_97046/154425054.html'):
    """
    章节内容
    :return:
    """
    html = ''
    if DEBUG is False:
        response = requests.get('http://www.b5200.net/%s' % path)
        if response.ok:
            html = response.text
    else:
        html = chapter_html

    root = etree.HTML(html)
    title_doc = root.xpath("//div[@class='bookname']/h1")
    content_doc = root.xpath("//div[@id='content']/p")
    catalog_doc = root.xpath("//div[@class='bottem2']/a[position()=3]/@href")
    previous_doc = root.xpath("//div[@class='bottem2']/a[position()=2]/@href")
    next_doc = root.xpath("//div[@class='bottem2']/a[position()=4]/@href")

    result = {
        'title': '',
        'article': [],
        'catalog': '',
        'previous': '',
        'next': ''
    }

    if isinstance(title_doc, list):
        result['title'] = title_doc[0].text.strip()

    if isinstance(content_doc, list) is False:
        print('没有找到')

    for row in content_doc:
        result['article'].append(row.text)

    if isinstance(catalog_doc, list):
        result['catalog'] = urlparse.urlsplit(catalog_doc[0]).path

    if isinstance(previous_doc, list):
        result['previous'] = urlparse.urlsplit(previous_doc[0]).path

    if isinstance(next_doc, list):
        result['next'] = urlparse.urlsplit(next_doc[0]).path

    return json.dumps(result, ensure_ascii=False)


def error(msg):
    print(msg)
    exit(0)
