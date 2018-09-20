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
        cls.loanID_PATH = os.path.join(Case_DIR + "\\config\\loanID.txt")

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


    @tag(Tag.FULL)
    def test_new_loan(self):
        """ 新建报单

        :return:
        """
        d = self.sess
        self.login(81,12345678)
        log.info('开始新建报单>>>>>>>>>>')
        d(resourceId="com.xiaoxiao.ludan:id/tv_menu", text=u"快速报单").click(timeout=10)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"合同费用").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").exists(timeout=5)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"合同费用").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").clear_text()
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"合同费用").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text(u"测试数据 - %s" % self.NowTime,timeout=2)
        d(scrollable=True).scroll.to(text="新增客户")
        d(resourceId="com.xiaoxiao.ludan:id/tv_edit_title",text="合同项目").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").clear_text()
        d(resourceId="com.xiaoxiao.ludan:id/tv_edit_title",text="合同项目").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text(u"测试数据 - %s" % self.NowTime,timeout=2)
        d.swipe(0.1, 0.9, 0.9, 0.1,duration=0.5)
        d(resourceId="com.xiaoxiao.ludan:id/tv_right").click_exists(timeout=5)
        log.info('本次随机生成的客户名称为：%s' % self.name)
        print('本次随机生成的客户名称为：%s' % self.name)
        log.info('本次随机生成的手机号码为：%s' % self.phone)
        print('本次随机生成的手机号码为：%s' % self.phone)
        log.info('本次随机生成的证件号码为：%s' % self.idcard)
        print('本次随机生成的证件号码为：%s' % self.idcard)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"姓名").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").exists(timeout=5)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"姓名").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").clear_text()
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"姓名").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text(self.name)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"手机号").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text(self.phone)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"证件类型").sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click()
        if d(resourceId="com.xiaoxiao.ludan:id/tv_type", text=u"香港身份证").exists(timeout=3) == True:
            d(resourceId="com.xiaoxiao.ludan:id/tv_type", text=u"香港身份证").click(timeout=5)
        else:
            self.d.ext_ocr.all()
            self.d.ext_ocr("香港身份证").click(timeout=3)
        d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"证件号码").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text(self.idcard)
        d(resourceId="com.xiaoxiao.ludan:id/right").click(timeout=5)
        if d(resourceId="com.xiaoxiao.ludan:id/title",text='快速报单').exists(timeout=3) == True:
            d(resourceId="com.xiaoxiao.ludan:id/right").click_exists(timeout=5)
            self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/title", text='报单详情').exists(timeout=3),msg=d.toast.get_message(10, 5))
            d(resourceId="com.xiaoxiao.ludan:id/iv_right").click_exists(timeout=10)
            d(text='新增贷款').click(timeout=5)
            if d(resourceId="com.xiaoxiao.ludan:id/title", text=u'贷款信息').exists(timeout=5) == True:
                log.info(d.toast.get_message(10, 5))
                print(d.toast.get_message(10, 5))
                d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u'申请银行').sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click(timeout=5)
                d(text='工商银行').click(timeout=5)
                d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u'银行产品').sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click(timeout=5)
                d(text='抵押贷').click(timeout=5)
                d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u'贷款类型').sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click(timeout=5)
                d(text='抵押贷').click(timeout=5)
                d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"申请金额").sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text('50000')
                # d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text='申请客户').sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click(timeout=5)
                d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u'按 揭 员').sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").click(timeout=5)
                d(text='黄蓉').click(timeout=5)
                d(resourceId="com.xiaoxiao.ludan:id/tv_yes").click(timeout=5)
                d(resourceId="com.xiaoxiao.ludan:id/tv_edit_title",text='备注:').sibling(resourceId="com.xiaoxiao.ludan:id/et_content").set_text(u"测试数据 - %s" % self.NowTime,timeout=2)
                d(resourceId="com.xiaoxiao.ludan:id/right").click(timeout=5)
                d(text='提交按揭部').click(timeout=5)
                if d(resourceId="com.xiaoxiao.ludan:id/title", text=u'报单详情').exists(timeout=5) == True:
                    log.info(d.toast.get_message(10, 5))
                    loanID = d(resourceId="com.xiaoxiao.ludan:id/tv_content_name", text=u"贷款编号：").sibling(resourceId="com.xiaoxiao.ludan:id/tv_content").get_text(timeout=5)
                    log.info('本次生成的贷款编号为：%s' % loanID)
                    print('本次生成的贷款编号为：%s' % loanID)
                    with open(self.loanID_PATH, 'w') as f:
                        f.write(loanID)
                else:
                    log.error('服务器返回：%s' % d.toast.get_message(10, 5))
                    print('服务器返回：%s' % d.toast.get_message(10, 5))
                    self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/title", text=u'报单详情').exists(),msg='服务器返回：%s' % d.toast.get_message(10, 5))
            else:
                log.error('服务器返回：%s' % d.toast.get_message(10, 5))
                print('服务器返回：%s' % d.toast.get_message(10, 5))
                self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/title", text=u'贷款信息').exists(),msg='服务器返回：%s' % d.toast.get_message(10, 5))
        else:
            log.error('服务器返回：%s' % d.toast.get_message(10, 5))
            print('服务器返回：%s' % d.toast.get_message(10, 5))
            self.assertTrue(d(resourceId="com.xiaoxiao.ludan:id/title",text='快速报单').exists(),msg='服务器返回：%s' % d.toast.get_message(10, 5))






if __name__ == '__main__':
    unittest.main()




