# -*- coding: utf-8 -*-
# @Author : Hami
import copy
import os.path

#  专门用例Yaml参数化
#  导入yaml的包： pip install pyyaml

# 读取yaml的数据
import yaml, os, uuid
from apirun.core.globalContext import g_context


def load_context_from_yaml(folder_path):
    """
    :param folder_path: 文件路径
    :return:
    """
    try:
        yaml_file_path = os.path.join(folder_path, "context.yaml")  # 把2个文本进行拼接
        with open(yaml_file_path, "r", encoding="utf-8") as f:
            #  加载所有数据
            data = yaml.load(f, Loader=yaml.FullLoader)
            print(f"装载yaml数据内容: ", data)
            # 如果数据不为空，则设置到全局变量当中
            if data: g_context().set_by_dict(data)
    except Exception as e:
        print(f"装载yaml文件错误: {str(e)}")
        return False


# 加载我们满足条件的文件及数据
def load_yaml_files(config_path):
    """
    返回满足条件的yaml文件列表及数据
    :param config_path: Yaml存放的路径
    :return:
    """

    yaml_caseInfos = []  # 存储所有的数据

    suite_folder = os.path.join(config_path)
    # 存放在该路径的全局变量进行写入
    load_context_from_yaml(suite_folder)
    # 满足条件的列表
    file_names = [(int(f.split("_")[0]), f) for f in os.listdir(suite_folder) if
                  f.endswith(".yaml") and f.split("_")[0].isdigit()]

    # 排序，排序只保留文件名即可
    file_names.sort()
    file_names = [f[-1] for f in file_names]

    # 加载每个文件的数据给到yaml_caseInfos
    for file_name in file_names:
        file_path = os.path.join(suite_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            #  加载所有数据
            caseinfo = yaml.full_load(f)
            yaml_caseInfos.append(caseinfo)  # [{yaml里面的数据}]
    return yaml_caseInfos  # 所有的测试用例


#  把yaml的格式处理成我们规定的格式
def yaml_case_parser(config_path):
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
    yaml_caseInfos = load_yaml_files(config_path)

    # TODO 2: 统一处理成一样的格式 （后面excel一样的处理）
    for caseinfo in yaml_caseInfos:

        # TODO 扩展: 获取ddt的数据，得到长度
        ddts = caseinfo.get("ddts", [])
        # TODO 扩展: 取到数据之后，我们需要删除ddts这个，避免有后续的影响
        if len(ddts) > 0:
            caseinfo.pop("ddts")

        if len(ddts) == 0:
            # 按照之前逻辑直接处理即可
            case_name = caseinfo.get("desc", uuid.uuid4().__str__())  # 没有名字，我们自己生成一个，需要把它写到我们测试用例当中
            caseinfo.update({"_case_name": case_name})  # 需要把它写到我们测试用例当中

            case_infos.append(caseinfo)  # 所有的测试用例 []
            case_names.append(case_name)  # 所有的用例名称 []
        else:
            # 根据ddts的数据生成多组数据
            for ddt in ddts:
                new_case = copy.deepcopy(caseinfo)
                # 给当前这个用例新增一个context对应值,没有的话则是一个空字典
                context = new_case.get("context", {})
                ddt.update(context)
                new_case.update({"context": ddt})

                # 用例值和对应的标题
                case_name = f'{caseinfo.get("desc", uuid.uuid4().__str__())}-{ddt.get("desc", uuid.uuid4().__str__())}'
                new_case.update({"_case_name": case_name})  # 需要把它写到我们测试用例当中

                case_infos.append(new_case)  # 所有的测试用例 []
                case_names.append(case_name)  # 所有的用例名称 []

    return {
        "case_infos": case_infos,
        "case_names": case_names
    }


# data = yaml_case_parser(r"F:\ProjectHcEdu\api_project_v2\day09\apirun_1\examples")
# print(data)
