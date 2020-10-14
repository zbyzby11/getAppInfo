#!/home/zhouheng/anaconda3/bin/python
# -*- encoding: utf-8 -*-
"""
@文件    :app.py
@说明    :
@时间    :2020/10/13 15:34:42
@作者    :周恒
@版本    :1.0
"""
from typing import *
import json


class App(object):
    def __init__(self, name: str, catagory: str, developer: str, description: str):
        super().__init__()
        self.name = name
        self.catagory = catagory
        self.developer = developer
        self.description = description

    @staticmethod
    def obj_to_json(app: "App") -> Dict:
        return {
            "name": app.name,
            "catagory": app.catagory,
            "developer": app.developer,
            "desc": app.description,
        }
