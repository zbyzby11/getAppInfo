#!/home/zhouheng/anaconda3/bin/python
# -*- encoding: utf-8 -*-
"""
@文件    :spider.py
@说明    :
@时间    :2020/10/13 11:51:52
@作者    :周恒
@版本    :1.0
"""


import aiohttp
import asyncio
import multiprocessing
from multiprocessing import Queue, Process
from typing import *
import re
import json
import logging
import requests
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s] - %(message)s",
)

logger = logging.getLogger(__name__)
APP_INFO_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=aaapfql80TZGPc_DAAztx; __utmc=127562001; __utmz=127562001.1602553038.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; t_id=noimeiweb_21fac106-fb4d-451a-b916-84e8e8b0cdde; Hm_lvt_765fefc2c357bae3970cea72e714811b=1602553038,1602553125,1602554734; __utma=127562001.1498534159.1602553038.1602557113.1602561973.3; __utmb=127562001.1.10.1602561973; Hm_lpvt_765fefc2c357bae3970cea72e714811b=1602561973",
    "Host": "app.mi.com",
    "Referer": "http://app.mi.com/category/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
}
APP_LIST_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=aaapfql80TZGPc_DAAztx; __utmc=127562001; __utmz=127562001.1602553038.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; t_id=noimeiweb_21fac106-fb4d-451a-b916-84e8e8b0cdde; Hm_lvt_765fefc2c357bae3970cea72e714811b=1602553038,1602553125,1602554734; __utma=127562001.1498534159.1602553038.1602553038.1602557113.2; __utmb=127562001.13.10.1602557113; Hm_lpvt_765fefc2c357bae3970cea72e714811b=1602558838",
    "Host": "app.mi.com",
    "Referer": "http://app.mi.com/category/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
APP_LIST_URL = (
    "http://app.mi.com/categotyAllListApi?page={0}&categoryId={1}&pageSize=30"
)
APP_INFO_URL = "http://app.mi.com/details?id={}"
CATAGORY = [i for i in range(1, 16)] + [27]


class Spider(object):
    def __init__(self, appInfoQueue: Queue):
        super().__init__()
        self.headers: Dict[str, str] = APP_LIST_HEADERS
        self.app_list_queue = Queue(100)  # (list,catagory id)
        self.app_info_queue = appInfoQueue

    @staticmethod
    def app_list_headers(catagoryId: int) -> Dict[str, str]:
        res = APP_LIST_HEADERS.copy()
        res["Referer"] += str(catagoryId)
        return res

    # async def get_app_list(self, categoryId: int, page: int) -> List:
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(
    #                 APP_LIST_URL.format(page, categoryId),
    #                 headers=Spider.app_list_headers(categoryId),
    #             ) as response:
    #                 text = await response.text()
    #                 self.app_list_queue.put((json.loads(text)["data"], categoryId))
    #     except Exception as e:
    #         logger.warning(e)
    #         return

    @staticmethod
    def app_info_headers(catagoryId: int) -> Dict[str, str]:
        res = APP_INFO_HEADER.copy()
        res["Referer"] += str(catagoryId)
        return res

    # async def get_app_info(self, package_name: str, catagoryId: int) -> str:
    #     try:
    #         resp = await aiohttp.request(
    #             "GET",
    #             package_name.format(package_name),
    #             headers=Spider.app_list_headers(catagoryId),
    #         )
    #         text = await resp.text()
    #         self.app_info_queue.put(text)
    #     except Exception as e:
    #         logger.info(e)

    # def get_app_list_process(self):
    #     tasks = []
    #     loop = asyncio.new_event_loop()
    #     for page in range(30):
    #         for cata in CATAGORY:
    #             tasks.append(self.get_app_list(cata, page))
    #     try:
    #         loop.run_until_complete(asyncio.wait(tasks))
    #     except Exception as e:
    #         logger.warning(e)

    # def get_app_info_process(self):
    #     loop = asyncio.new_event_loop()
    #     tasks = []
    #     while True:
    #         try:
    #             for i in range(10):
    #                 e = self.app_info_queue.get(timeout=10)
    #                 tasks.append(self.get_app_info(e[0]["packageName"], e[1]))
    #         except Exception as e:
    #             logger.warning(e)
    #         finally:
    #             loop.run_until_complete(asyncio.wait(tasks))
    #             return
    #         loop.run_until_complete(asyncio.wait(tasks))

    # def run_async(self):
    #     processes: List[Process] = [
    #         Process(target=self.get_app_list_process, args=())
    #         for i in range(multiprocessing.cpu_count())
    #     ] + [
    #         Process(target=self.get_app_info_process, args=())
    #         for i in range(multiprocessing.cpu_count())
    #     ]
    #     for process in processes:
    #         process.start()
    #     for process in processes:
    #         process.join()

    def run_slowly(self):
        for page in range(10):
            for catagory in CATAGORY:
                try:
                    text = requests.get(
                        APP_LIST_URL.format(page,catagory),
                        headers=Spider.app_list_headers(catagory),
                    ).text
                    time.sleep(2)
                    l = json.loads(text)["data"]
                    try:
                        for i in range(len(l)):
                            text1 = requests.get(
                                APP_INFO_URL.format(l[i]["packageName"]),
                                headers=Spider.app_info_headers(catagory),
                            ).text
                            self.app_info_queue.put((text1,catagory,l[i]["displayName"],catagory))
                            time.sleep(2)
                    except Exception as e:
                        logger.warning(e)
                        
                except Exception as e:
                    logger.warning(e)
                    # e.with_traceback()
                    # c=input()
