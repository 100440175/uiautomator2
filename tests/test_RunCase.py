#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utx import *

if __name__ == '__main__':
    setting.run_case = {Tag.SMOKE}  # 只运行SMOKE冒烟用例
    # setting.run_case = {Tag.FULL}  # 运行全部测试用例
    # setting.run_case = {Tag.SMOKE, Tag.SP}   # 只运行标记为SMOKE和SP的用例

    runner = TestRunner()
    runner.add_case_dir(r"D:\Code\uiautomator2\examples\com.xiaoxiao.ludan")
    runner.run_test(report_title='自动化测试报告')



