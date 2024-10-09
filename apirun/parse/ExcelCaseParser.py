# -*- coding: utf-8 -*-
# @Author : Hami
import ast
import copy
import json
import os.path

#  专门用例Excel参数化
#  导入excel的包：pip install pandas
# openpyxl是pandas用于读取.xlsx文件的引擎之一
# pip install pandas openpyxl

# 读取yaml的数据
import yaml, os, uuid
import pandas as pd
from apirun.core.globalContext import g_context


def load_context_from_excel(folder_path):
    """
    :param folder_path: 文件路径
    :return:
    """
    try:
        excel_file_path = os.path.join(folder_path, "context.xlsx")  # 把2个文本进行拼接
        # 读取excel
        df = pd.read_excel(excel_file_path)
        # 初始化一个变量进行存储
        data = {
            "_database": {}
        }
        for index, row in df.iterrows():
            # 如果是变量我们就直接存在：变量名：value
            if row["类型"] == "变量":
                data[row["变量描述"]] = row["变量值"]
            elif row["类型"] == "数据库":
                db_name = row["变量描述"]
                db_config = json.loads(row["变量值"])  # 变成字典格式
                data["_database"][db_name] = db_config
        if data: g_context().set_by_dict(data)  # 写入到全局变量
    except Exception as e:
        print(f"装载excel文件错误: {str(e)}")
        return False


# 加载我们满足条件的文件及数据
def load_excel_files(config_path):
    """
    返回满足条件的excel文件列表及数据
    :param config_path: excel存放的路径
    :return:
    """

    excel_caseInfos = []  # 存储所有的数据

    suite_folder = os.path.join(config_path)
    # 存放在该路径的全局变量进行写入
    load_context_from_excel(suite_folder)
    # 满足条件的列表
    file_names = [(int(f.split("_")[0]), f) for f in os.listdir(suite_folder) if
                  f.endswith(".xlsx") and f.split("_")[0].isdigit()]

    # 排序，排序只保留文件名即可
    file_names.sort()
    file_names = [f[-1] for f in file_names]

    # 读取我们维护的yaml数据，方便后面和值一一对应起来
    current_dir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
    parent_dir = os.path.dirname(current_dir)  # 基于当前路径获取上一层路径
    keywords_file_path = os.path.join(parent_dir, "extend/keywords.yaml")  # 进行拼接

    keywords_info = {}
    with open(keywords_file_path, "r", encoding="utf-8") as f:
        keywords_info = yaml.full_load(f)  #

    # 加载每个文件的数据给到yaml_caseInfos
    for file_name in file_names:
        file_path = os.path.join(suite_folder, file_name)
        # TODO 1: 读取excel
        data = pd.read_excel(file_path, sheet_name=0)
        data = data.where(data.notnull(), None)  # 将非空值保留，空数据用None替换
        data = data.to_dict(orient='records')  # 以字典的格式给我显示

        # 初始化一个字典，用例存放某一条测试用例
        current_test_case = None

        for row in data:
            # print(row)
            # 判断是否有测试标题：如果有的话，代表是我们第一个，直到遇到下一个标题，就从头开头

            # TODO 1: # 检查当前行是否包含有效的测试用例标题，有则代表对应的起始位
            if pd.notna(row["测试用例标题"]):
                # 如果已经构建完毕那么需要当前加进去到对应的测试用例当中
                if current_test_case is not None:
                    excel_caseInfos.append(current_test_case)

                # 初始化一个测试用例字典
                current_test_case = {
                    "desc": row['测试用例标题'],
                    "featureName": row['一级模块'],
                    "storyName": row['二级模块'],
                    "steps": []
                }

            # TODO 2-1: 初始化步骤的值
            steps = {
                row["步骤描述"]: {
                    "关键字": row["关键字"]
                }
            }
            # TODO 2-2: 考虑步骤当中对应的每个参数。
            parameter = []
            for key, value in row.items():
                if "参数_" in key:
                    try:
                        # 尝试将字符串转换为Python对象
                        value = ast.literal_eval(value)
                    except:
                        pass
                    parameter.append(value)

            # TODO 2-3: 把对应的值和KEY一一对应起来，这样我们才能发送请求 -zip
            # dict_parameter = {k,v  for k,v in zip(key,value)}
            dict_parameter = {k: v for k, v in zip(keywords_info[row["关键字"]], parameter)}
            steps[row["步骤描述"]].update(dict_parameter)

            # 步骤加到当前测试用例来
            current_test_case["steps"].append(steps)

        if current_test_case is not None:
            excel_caseInfos.append(current_test_case)

    return excel_caseInfos


#  把yaml的格式处理成我们规定的格式
def excel_case_parser(config_path):
    """
    返回指定条件的格式
    :param config_path:  文件的路径
    :return: {
            "case_infos": case_infos,  #  所有的测试用例 []
            "case_names": case_names   #  所有测试用例对应的标题 []
            }
    """
    # TODO 0: 对应固定的格式
    case_infos = []
    case_names = []

    # TODO 1: 调用对应的方法：拿到所有的用例数据
    excel_caseInfos = load_excel_files(config_path)

    # TODO 2: 统一处理成一样的格式 （后面excel一样的处理）
    for caseinfo in excel_caseInfos:
        caseinfo.update({"_case_name": caseinfo["desc"]})
        case_infos.append(caseinfo)  # 所有的测试用例 []
        case_names.append(caseinfo["desc"])  # 所有的用例名称 []

    return {
        "case_infos": case_infos,
        "case_names": case_names
    }


# data = load_excel_files(r"F:\ProjectHcEdu\api_project_v2\day09\apirun_1\examples")
# print(data)
