# -*- coding: utf-8 -*-
# @Author : Hami

# 文件名必须这个，不能改。
# 钩子函数都是框架自带的。pytest的钩子函数

import pytest
import logging
import allure
import jsonpath
import requests

# TODO 扩展：导入我们封装的关键字
from apirun.extend.keywords import KeyWords

keywords = KeyWords()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 通过 out = yield 定义了一个生成器。在生成器中，res = out.get_result() 获取了测试结果对象。
    out = yield  #  类似于return，但是它返回之后执行完毕会自动回来
    res = out.get_result()
    #  res.when == "call"：表示正在运行调用测试函数的阶段。
    if res.when == "call":
        logging.info(f"用例ID：{res.nodeid}")
        logging.info(f"测试结果：{res.outcome}")
        logging.info(f"故障表示：{res.longrepr}")
        logging.info(f"异常：{call.excinfo}")
        logging.info(f"用例耗时：{res.duration}")
        logging.info("**************************************")


# 就是一个普通的方法，这个特殊点，在测试之前或者之后做一些事情
# 不需要人工去进行调用，自己去进行调用。
@pytest.fixture(scope="session")
def token_fix():
    # 登录代码一系列的事情
    # TODO 1 : 登录
    with allure.step("第一步：进行登录操作"):
        url = "http://shop-xo.hctestedu.com/index.php?s=/api/user/login"
        pub_params = {"application": "app", "application_client_type": "weixin"}  # 以字典的格式去写
        data = {"accounts": "hami", "pwd": "123456", "type": "username"}

        # 发送请求的
        # res = requests.post(url, params=pub_params, data=data)
        res = keywords.request_post(url=url, params=pub_params, data=data)

        # TODO 1: 获取我们响应数据:msg
        # 注意: 返回的数据一定是一个列表,需要下标
        msg_res = jsonpath.jsonpath(res.json(), "$..msg")[0]
        print("当前提取的数据为:", msg_res)

        # TODO 2: 通过对应的msg进行断言处理
        assert msg_res == "登录成功", f"当前msg的信息是:{msg_res}"

        # TODO 3: 获取对应的token数据
        token_res = jsonpath.jsonpath(res.json(), "$..token")[0]
        print("当前提取的数据为:", token_res)
        print("----------------------------------")
        return token_res
