# -*- coding: utf-8 -*-
# @Author : Hami
import os.path

# 导入对应的参数化方法
from apirun.parse.YamlCaseParser import yaml_case_parser
from apirun.parse.ExcelCaseParser import excel_case_parser


def case_parser(case_type, case_dir):
    """

    :param case_type: 用例的类型：yaml、 excel
    :param case_dir: 用例所在的文件夹
    :return: 调用方法是什么返回的格式就是什么：返回 {"case_name":[], "cases_info":[]}
    """

    config_path = os.path.abspath(case_dir)

    if case_type == "yaml":
        return yaml_case_parser(config_path)
    if case_type == "excel":
        return excel_case_parser(config_path)

    # 如果上面执行完毕，都不满足条件，则返回空
    return {"case_name": [], "cases_info": []}

# data = case_parser("yaml","../examples")
# print(data)
