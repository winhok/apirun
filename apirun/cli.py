# -*- coding: utf-8 -*-

# TODO 代码参考如下：生成allure测试报告
import pytest
import os, sys
from apirun.core.CasesPlugin import CasesPlugin
from allure_combine import combine_allure


def run():
    # 获取 python运行参数
    # 1. 读取命令行传入的参数
    pytest_cmd_config = []
    for arg in sys.argv:
        if arg.startswith("-"):
            pytest_cmd_config.append(arg)

    print(os.path.join(os.path.dirname(__file__), "core/ApiTestRunner.py"))

    # 2. 构建pytest参数
    pytest_args = [os.path.join(os.path.dirname(__file__), "core/ApiTestRunner.py")]
    pytest_args.extend(pytest_cmd_config)

    print("run pytest：", pytest_args)

    pytest.main(pytest_args, plugins=[CasesPlugin()])


if __name__ == '__main__':
    pytest_args = ["-v", "-s", "--capture=sys",  # 用于显示输出调试信息、 设置级别、打开实时输出
                   "./core/ApiTestRunner.py",  # 指定对应的执行文件
                   "--clean-alluredir",  # 清空alluredir中的历史数据
                   "--alluredir=allure-results",  # 执行过程的数据存放到allure-results中
                   "--type=yaml",  # 指定文件运行类型
                   "--cases=..\examples\error_back"  # 指定运行的路径
                   # "--cases=..\examples\dsw-yaml"  # 指定运行的路径
                   ]

    print("run pytest：", pytest_args)
    pytest.main(pytest_args, plugins=[CasesPlugin()])
    os.system(r"allure generate -c -o allure-report")  # 等于你在命令行里面执行 allure

    # TODO 3: 代码参考如下：生成allure测试报告，双击打开直接查看 combine_allure(测试报告的路径)
    combine_allure("./allure-report")
