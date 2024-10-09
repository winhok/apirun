# -*- coding: utf-8 -*-
# @Author : Hami
import copy
import json

import allure
import pytest

# 核心执行器
from apirun.parse.YamlCaseParser import load_yaml_files
from apirun.parse.CaseParser import case_parser
from apirun.extend.keywords import KeyWords
from apirun.utils.VarRender import refresh  # 变量渲染方法
from apirun.utils.DynamicTitle import dynamicTitle  # 变量渲染方法
from apirun.core.globalContext import g_context  # 全局变量


class TestRunner:
    # TODO 1: 读取到对应的数据
    # caseinfo = case_parser("excel","./examples") #  参数

    # TODO 2:
    # @pytest.mark.parametrize("caseinfo", caseinfo["case_infos"])
    def test_case_execute(self, caseinfo):
        print("当前的测试数据：", caseinfo)
        # TODO 2-1: 动态生成一下当前的测试用例标题
        # allure.dynamic.title(caseinfo["_case_name"])

        # TODO 2-1 : 调用动态生成标题的方法
        dynamicTitle(caseinfo)

        # TODO 2-2: 基于我们步骤一步步进行执行
        try:
            # 实例化关键字对象
            keywords = KeyWords()

            # 获取当前用例变量，方便后续的渲染
            local_context = caseinfo.get("context",{})
            context = copy.deepcopy(g_context().show_dict())
            context.update(local_context)

            steps = caseinfo.get("steps", None)
            for step in steps:
                #  提示信息
                step_name = list(step.keys())[0]
                step_value = list(step.values())[0]
                print(f"开始执行步骤：{step_name} - {step_value}")

                # TODO : 每一个步骤进行变量的渲染
                context = copy.deepcopy(g_context().show_dict())
                context.update(local_context)
                step_value = eval(refresh(step_value, context))

                # 基于每个步骤的关键字，找到对应的方法，然后把参数给它
                #  通过【反射】的方式去找到对应的方法
                with allure.step(step_name):
                    key = step_value["关键字"]  # 具体的方法名, 在 keywords 里面找到这个方法
                    try:
                        key_func = keywords.__getattribute__(key)  # 从keywords获取到对应方法
                    except AttributeError as e:
                        print("没有这个关键字方法", e)
                    key_func(**step_value)  # 调用方法
        finally:
            print("--当前步骤执行结束--")
