# coding: utf-8
import logging

import uiautomator2 as u2
import unittest
import time

from utx import *


class SimpleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = u2.connect_wifi('192.168.11.125')
        cls.d.set_orientation('natural')
        cls.d.healthcheck()
        cls.d.implicitly_wait(10)
        cls.d.app_clear("com.xiaoxiao.ludan")
        cls.d.app_stop_all()


    def setUp(self):
        self.d.set_fastinput_ime(True)
        self.sess = self.d.session("com.xiaoxiao.ludan")

    def tearDown(self):
        self.d.app_clear("com.xiaoxiao.ludan")
        self.d.app_stop_all()

    def login(self,username,password):
        d = self.sess
        d.watchers.remove()
        d.watchers.watched = False
        d.watcher("获取app权限").when(resourceId="android:id/button1").when(text="允许").click(text="允许")
        d.watchers.run()
        d(resourceId="com.xiaoxiao.ludan:id/et_account").set_text(username,timeout=10)
        d(resourceId="com.xiaoxiao.ludan:id/et_password").set_text(password,timeout=5)
        d(resourceId="com.xiaoxiao.ludan:id/bt_login").click_exists(timeout=5)
        if d(resourceId="com.xiaoxiao.ludan:id/title").exists(timeout=5) == True:
            d(resourceId="com.xiaoxiao.ludan:id/ed_vc").set_text('8888',timeout=5)
            d(resourceId="com.xiaoxiao.ludan:id/tv_sign").click(timeout=5)
        else:
            pass
        if d(text=u"首页").exists(timeout=5) == True:
            log.info(d.toast.get_message(10, 10))
        else:
            log.error(d.toast.get_message(10, 10))




    @tag(Tag.FULL)
    def test_login(self):
        """ 测试登录

        :return:
        """
        self.login(69,12345678)


if __name__ == '__main__':
    unittest.main()
