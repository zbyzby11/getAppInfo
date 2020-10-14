#!/home/zhouheng/anaconda3/bin/python
# -*- encoding: utf-8 -*-
"""
@文件    :parser.py
@说明    :
@时间    :2020/10/13 14:00:19
@作者    :周恒
@版本    :1.0
"""
import multiprocessing
from multiprocessing import Queue
import json
from typing import *
from app import App
import bs4
import re
from lxml import etree
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s] - %(message)s",
)

logger = logging.getLogger(__name__)



class Parser(object):
    def __init__(self, textQueue: Queue, fp):
        super().__init__()
        self.text_queue = textQueue
        self.fp = fp
        self.catagory_selector = "body > div.main > div.container.cf > div.bread-crumb > ul > li:nth-child(2) > a"
        self.developer_selector = "body > div.main > div.container.cf > div:nth-child(6) > div.float-right > div:nth-child(2)"

    def extract(self):
        while True:
            try:
                e = self.text_queue.get(timeout=20)
                logger.info("{0}{1}".format(e[1], e[2]))
            except Exception as e:
                logger.warning(e)
                return
            try:
                bs = bs4.BeautifulSoup(e[0], "lxml")
                desc = (
                    bs.findAll("div", class_="app-text")[0]
                    .findAll("p", class_="pslide")[0]
                    .text
                )
                developer = bs.select(self.developer_selector)[0].text
                catagory = bs.select(self.catagory_selector)[0].text
                logger.info(desc)
                self.fp.write(
                    json.dumps(
                        App(e[2], catagory, developer, desc),
                        default=App.obj_to_json,
                        ensure_ascii=False,
                    )
                    + ",\n"
                )
                self.fp.flush()
            except Exception as e:
                logger.warning(e)

    def work_process(self):
        while True:
            try:
                text = self.text_queue.get(timeout=20)
                app = self.extract(text)
                self.app_queue.put(app)
                try:
                    pass
                except Exception as e:
                    logger.info(e)
            except Exception as e:
                logger.info(e)
                return


if __name__ == "__main__":
    f = open("/home/zhouheng/details.html", "r", encoding="utf-8")
    s = f.read()
    p = re.compile(
        '<div style="float: left">开发者</div><div style="float:right;">(.*?)</div>'
    )
    print(re.findall(p, s))
    f.seek(0)
    bs = bs4.BeautifulSoup(f, "lxml")

    bs = bs.select(
        "body > div.main > div.container.cf > div.bread-crumb > ul > li:nth-child(2) > a"
    )[0]
    # print(bs.findAll("p", class_="pslide")[0].text)
    print(bs.text)
    f.close()
    # html = etree.parse("/home/zhouheng/details.html", etree.HTMLParser())
    # res = html.xpath("/html/body/div[6]/div[1]/div[8]")
    # for i in res:
    #     print(i.text)
