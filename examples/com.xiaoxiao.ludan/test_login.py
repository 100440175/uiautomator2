# coding: utf-8


import uiautomator2 as u2
import unittest
import time

from utx import *


class SimpleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = u2.connect_usb('127.0.0.1:62001')
        cls.d.set_orientation('natural')
        cls.d.implicitly_wait(10)

    def setUp(self):
        self.sess = self.d.session("com.xiaoxiao.ludan")
        self.sess.watchers.remove()

    def tearDown(self):
        self.sess.watchers.remove()
        self.d.app_clear("com.xiaoxiao.ludan")
        self.d.app_stop_all()

    @tag(Tag.SMOKE)
    def test_login(self,username,password):
        """ 测试登录

        :return:
        """
        d = self.sess
        d(resourceId="com.xiaoxiao.ludan:id/et_account").set_text(username,timeout=10)
        d(resourceId="com.xiaoxiao.ludan:id/et_password").set_text(password,timeout=5)
        d(resourceId="com.xiaoxiao.ludan:id/bt_login").click_exists(timeout=5)
        if d(resourceId="com.xiaoxiao.ludan:id/title").exists(timeout=10) == True:
            d(resourceId="com.xiaoxiao.ludan:id/ed_vc").set_text('8888',timeout=5)
            d(resourceId="com.xiaoxiao.ludan:id/tv_sign").click(timeout=5)
            d.toast.get_message(0, 0.4)
        else:
            d.toast.get_message(0, 0.4)
            pass
        self.assertEqual(d.toast.get_message(2, 5, ""), "登录成功，数据加载完成")


if __name__ == '__main__':
    unittest.main()
