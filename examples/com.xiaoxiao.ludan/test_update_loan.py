#!/usr/bin/env python
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config.random_date import *
import uiautomator2 as u2
import unittest
import time
from utx import *
import uiautomator2.ext.ocr as ocr


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = u2.connect()
        ocr.API = "http://ocr.open.netease.com/api/ocr"
        u2.plugin_register("ocr", ocr.OCR)
        cls.d.set_orientation('natural')
        cls.d.healthcheck()
        cls.d.implicitly_wait(10)
        cls.d.app_clear("com.xiaoxiao.ludan")
        cls.d.app_stop_all()
        cls.NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cls.test_random = test_random_date()
        Case_DIR = os.path.abspath(os.path.dirname(__file__))
        cls.loanID_PATH = os.path.join(Case_DIR + "\\config\\loan_info.txt")


    def setUp(self):
        self.d.set_fastinput_ime(True)
        self.sess = self.d.session("com.xiaoxiao.ludan")
        self.name = self.test_random.get_name()
        self.phone = self.test_random.createPhone()
        self.idcard = self.test_random.idcard_generator()

    def tearDown(self):
        self.d.app_stop_all()
        self.d.set_fastinput_ime(False)

    def login(self,username,password):
        d = self.sess
        d.watchers.remove()
        d.watchers.watched = False
        log.info('开始登录>>>>>>>>>>')
        d.watcher("获取app权限").when(resourceId="android:id/button1").when(text="允许").click(text="允许")
        d.watchers.run()
        d(resourceId="com.xiaoxiao.ludan:id/et_account").set_text(username,timeout=10)
        d(resourceId="com.xiaoxiao.ludan:id/et_password").set_text(password,timeout=5)
        d(resourceId="com.xiaoxiao.ludan:id/bt_login").click_exists(timeout=5)
        if d(resourceId="com.xiaoxiao.ludan:id/title").exists(timeout=2) == True:
            d(resourceId="com.xiaoxiao.ludan:id/ed_vc").set_text('8888',timeout=5)
            d(resourceId="com.xiaoxiao.ludan:id/tv_sign").click(timeout=5)
        else:
            pass
        self.assertTrue(d(text=u"首页").exists(timeout=3),msg=d.toast.get_message(10, 5))
        log.info('服务器返回：%s' % d.toast.get_message(10, 10))
        print('服务器返回：%s' % d.toast.get_message(10, 10))


    @tag(Tag.Encoding)
    def test_update_loan(self):
        """ 按揭员更新贷款

        :return:
        """
        d = self.sess
        self.login(69,12345678)
        log.info('开始更新贷款>>>>>>>>>>')
        d(resourceId="com.xiaoxiao.ludan:id/tv_menu", text=u"贷款跟进").click(timeout=10)
        self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/et_pact_search").exists(timeout=3),msg=d.toast.get_message(10, 5))
        if d(resourceId="com.xiaoxiao.ludan:id/tv_search_type",text='客户名').exists() == True:
            d(resourceId="com.xiaoxiao.ludan:id/tv_search_type", text='客户名').click()
        else:
            self.d.ext_ocr.all()
            self.d.ext_ocr("客户名").click(timeout=3)
        d(text=u"贷款号").click(timeout=2)
        with open(self.loanID_PATH, 'r') as f:
            loan_id = f.read()
            log.info('本次待更新的贷款编号为：%s' % loan_id)
            print('本次待更新的贷款编号为：%s' % loan_id)
        d(resourceId="com.xiaoxiao.ludan:id/et_pact_search").clear_text()
        d(resourceId="com.xiaoxiao.ludan:id/et_pact_search").set_text(loan_id)
        self.d.set_fastinput_ime(False)
        d.send_action('search')
        self.d.set_fastinput_ime(True)
        self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/tv_loan_numb",text='%s' % loan_id).exists(timeout=5),msg=d.toast.get_message(10, 5))
        d(resourceId="com.xiaoxiao.ludan:id/tv_loan_numb", text='%s' % loan_id).click()
        d(resourceId="com.xiaoxiao.ludan:id/title",text='贷款详情').exists(timeout=3)
        d(resourceId="com.xiaoxiao.ludan:id/iv_add").click()
        d(resourceId="com.xiaoxiao.ludan:id/tv_bt_content",text='跟进').click(timeout=5)
        self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/title",text='已签约待面签').exists(timeout=5),msg=d.toast.get_message(10, 5))
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name",text='银行经理').sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click()
        d(text='猴赛雷').click(timeout=3)
        d(resourceId="com.xiaoxiao.ludan:id/tv_edit_title",text='备注').sibling('com.xiaoxiao.ludan:id/et_content').set_text(u"测试数据 - %s" % self.NowTime,timeout=2)
        d(resourceId="com.xiaoxiao.ludan:id/tv_add_manager").click()
        self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/title", text='贷款详情').exists(timeout=2),msg=d.toast.get_message(10, 5))


if __name__ == '__main__':
    unittest.main()


