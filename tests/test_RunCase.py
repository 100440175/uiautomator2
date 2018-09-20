#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os

from utx import *

if __name__ == '__main__':
    setting.run_case = {Tag.FULL}
    # setting.run_case = {Tag.FULL}   # 运行全部测试用例
    # setting.run_case = {Tag.SMOKE}  # 只运行SMOKE标记的测试用例
    # setting.run_case = {Tag.SMOKE, Tag.SP}   # 只运行SMOKE和SP标记的测试用例
    setting.show_error_traceback = True  # 执行用例的时候，显示报错信息
    full_case_name = True   # 显示完整用例名字（函数名字+参数信息）
    setting.sort_case = True  # 是否按照编写顺序，对用例进行排序
    log.set_level(logging.DEBUG)  # 设置utx的log级别
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    case_dir = os.path.join(path + "\\examples\\com.xiaoxiao.ludan")

    runner = TestRunner()
    runner.add_case_dir(case_dir)
    runner.run_test(report_title='自动化测试报告')



