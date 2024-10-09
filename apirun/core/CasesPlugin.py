# -*- coding: utf-8 -*-
# @Author : Hami
from apirun.parse.CaseParser import case_parser


# 放我们自定义的参数
class CasesPlugin:
    """
    这里的方法名都不能改名字，因为用的是钩子函数
    是 pytest 自带的，会在执行用例之前，自己去进行调用的。
    """

    def pytest_addoption(self, parser):
        """
        增加pytest运行的配置项
        :param parser:
        :return:
        """
        parser.addoption("--type", action="store", default="yaml", help="测试用例类型")
        parser.addoption("--cases", action="store", default="./examples", help="测试用例目录")

    def pytest_generate_tests(self, metafunc):
        """
         主要用来生成测试用例的，相当于 参数化。
        :param metafunc:
        :return:
        """
        # 读取用户传过来的参数
        case_type = metafunc.config.getoption("type")  # 类型
        cases_dir = metafunc.config.getoption("cases")  # 路径

        # 调用方法
        data = case_parser(case_type, cases_dir)

        # 进行测试用例进行参数化，自动交给runner去进行执行执行
        if "caseinfo" in metafunc.fixturenames:
            metafunc.parametrize("caseinfo", data["case_infos"], ids=data["case_names"])
