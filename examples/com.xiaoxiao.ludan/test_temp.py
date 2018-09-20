#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import unittest

import uiautomator2 as u2
import uiautomator2.ext.ocr as ocr
import random
from utx import *

class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = u2.connect()
        cls.d.set_orientation('natural')
        cls.d.healthcheck()
        cls.d.implicitly_wait(10)
        cls.d.app_clear("com.xiaoxiao.ludan")
        cls.d.app_stop_all()
        ocr.API = "http://ocr.open.netease.com/api/ocr"
        u2.plugin_register("ocr", ocr.OCR)



    def setUp(self):
        self.d.set_fastinput_ime(True)
        self.sess = self.d.session("com.xiaoxiao.ludan")

    def tearDown(self):
        self.d.app_clear("com.xiaoxiao.ludan")
        self.d.app_stop_all()

    # def test_000(self):
    #     self.d.ext_ocr.all()
    #     self.d.ext_ocr("登录").click()
    #     print('OCR')
    # output
    # ('状态', 138, 1888),
    # ('运动', 408, 1888),
    # ('发现', 678, 1888),
    # ('我的', 948, 1888)]
    # d.ext_ocr("我的").click() # 点击带有"我的" 的按钮


    # @tag(Tag.temp)
    # def test_idcard_generator(self):
    #     """ 随机生成新的18为身份证号码 """
    #     ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    #     LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    #     t = time.localtime()[0]
    #     x = '%02d%02d%02d%04d%02d%02d%03d' % (
    #     random.randint(10, 99), random.randint(1, 99), random.randint(1, 99), random.randint(t - 80, t - 18),
    #     random.randint(1, 12), random.randint(1, 28), random.randint(1, 999))
    #     y = 0
    #     for i in range(17):
    #         y += int(x[i]) * ARR[i]
    #     IDCard = '%s%s' % (x, LAST[y % 11])
    #     # birthday = '%s-%s-%s 00:00:00' % (IDCard[6:14][0:4], IDCard[6:14][4: 6], IDCard[6:14][6:8])
    #     print(IDCard)
    #     log.info(IDCard)
    #     return IDCard






if __name__ == '__main__':
    unittest.main()





