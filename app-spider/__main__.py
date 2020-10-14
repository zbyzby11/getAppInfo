#!/home/zhouheng/anaconda3/bin/python
# -*- encoding: utf-8 -*-
"""
@文件    :__main__.py
@说明    :
@时间    :2020/10/13 13:58:50
@作者    :周恒
@版本    :1.0
"""


from spider import Spider
from parser import Parser
import asyncio
import multiprocessing
from multiprocessing import Queue, Process

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s] - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    f = open("data.json", "w", encoding="utf-8")
    f.write("[")
    q = Queue(10)
    s = Spider(q)
    parser = Parser(q, f)
    p = Process(target=parser.extract, args=())
    p.start()
    s.run_slowly()
    p.join()
    



main()
