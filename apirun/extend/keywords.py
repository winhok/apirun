# -*- coding: utf-8 -*-
# @Author : Hami

"""
    这是接口关键字驱动类，用于提供自动化接口测试的关键字方法。
    主要是实现常用的关键字内容，并定义好所有的参数内容即可
    接口中常用关键字：
        1.各种模拟请求方法：Post/get/put/delete/header/....
        2.根据需求进行断言封装：jsonpath、数据库断言
        3.集合Allure，可添加@allure.step，这样在自动化执行的时候
        Allure报告可以直接捕捉相关的执行信息，让测试报告更详细
"""
import json
import random

import allure
import requests
import jsonpath
from apirun.core.globalContext import g_context
from deepdiff import DeepDiff
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class KeyWords:
    request = None

    @allure.step("参数数据：发送Post请求")
    def request_post(self, **kwargs):
        response = requests.post(**kwargs)
        # TODO: 扩展- 把对应的响应数据写到变量渲染中
        g_context().set_dict("current_response", response)  # 默认设置成变量渲染
        return response

    # @allure.step("参数数据：发送Get请求")
    # def request_get(self, **kwargs):
    #     response = requests.get(**kwargs)
    #     # TODO: 扩展- 把对应的响应数据写到变量渲染中
    #     g_context().set_dict("current_response", response)  # 默认设置成变量渲染
    #     return response

    @allure.step("参数数据：发送Get请求")
    def request_get(self, **kwargs):
        url = kwargs.get("URL", None)
        params = kwargs.get("PARAMS", None)
        headers = kwargs.get("HEADERS", None)

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
        }

        response = requests.get(**request_data)
        g_context().set_dict("current_response", response)  # 默认设置成全局变量
        return response
        print("-----------------------")
        print(response.json())
        print("-----------------------")

    @allure.step("参数数据：发送Post请求-form_urlencoded")
    def request_post_form_urlencoded(self, **kwargs):
        """
        发送Post请求
        """
        url = kwargs.get("URL", None)
        params = kwargs.get("PARAMS", None)
        headers = kwargs.get("HEADERS", None)
        data = kwargs.get("DATA", None)

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "data": data,
        }

        response = requests.post(**request_data)
        g_context().set_dict("current_response", response)  # 默认设置成全局变量
        return response
        print("-----------------------")
        print(response.json())
        print("-----------------------")

    @allure.step("参数数据：发送Post请求-row_json")
    def request_post_row_json(self, **kwargs):
        """
        发送Post请求
        """
        url = kwargs.get("URL", None)
        params = kwargs.get("PARAMS", None)
        headers = kwargs.get("HEADERS", None)
        data = kwargs.get("DATA", None)

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "json": data,
        }

        response = requests.post(**request_data)
        g_context().set_dict("current_response", response)  # 默认设置成全局变量
        return response
        print("-----------------------")
        print(response.json())
        print("-----------------------")

    @allure.step("参数数据：发送Post请求-form_data")
    def request_post_form_data(self, **kwargs):
        """
        发送Post请求
        """
        url = kwargs.get("URL", None)
        files = kwargs.get("FILES", None)
        params = kwargs.get("PARAMS", None)
        headers = kwargs.get("HEADERS", None)
        data = kwargs.get("DATA", None)

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "data": data,
            "files": eval(files)  # 变成字典格式
        }

        response = requests.post(**request_data)
        print("response",response.json())
        g_context().set_dict("current_response", response)  # 默认设置成全局变量
        return response
        print("-----------------------")
        print(response.json())
        print("-----------------------")

    @allure.step("参数数据：发送Delete请求")
    def request_delete(self, **kwargs):
        """
        发送Post请求
        """
        url = kwargs.get("URL", None)
        params = kwargs.get("PARAMS", None)
        headers = kwargs.get("HEADERS", None)
        data = kwargs.get("DATA", None)

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "json": data,
        }

        response = requests.delete(**request_data)
        g_context().set_dict("current_response", response)  # 默认设置成全局变量
        return response
        print("-----------------------")
        print(response.json())
        print("-----------------------")

    # TODO: 扩展 - JAONPATH提取的方法
    @allure.step("参数数据：提取响应数据并存储")
    def ex_jsonData(self, **kwargs):
        """
        提取json数据
        EXVALUE：提取josn的表达式
        INDEX: 非必填，默认为0,all代表所有
        VARNAME：存储的变量名，方便后面使用
        """
        # 获取JsonPath的值
        EXPRESSION = kwargs.get("EXVALUE", None)
        # 获取对应的下标，非必填，默认为0
        INDEX = kwargs.get("INDEX", 0)
        if INDEX is None:
            INDEX = 0
        # 获取响应数据
        response = g_context().get_dict("current_response").json()

        if INDEX == "all":
            ex_data = jsonpath.jsonpath(response, EXPRESSION)
        else:
            ex_data = jsonpath.jsonpath(response, EXPRESSION)[INDEX]  # 通过JsonPath进行提取
        g_context().set_dict(kwargs["VARNAME"], ex_data)  # 根据变量名设置成变量渲染
        print("-----------------------")
        print(g_context().show_dict())
        print("-----------------------")
        return ex_data

    # TODO: 扩展 - 数据库提取的方法
    @allure.step("参数数据：提取数据库数据并存储")
    def ex_mysqlData(self, **kwargs):
        """
        数据库 : 数据库的名称
        引用变量：数据库要存储的变量名，列表格式
        存储到全局变量：{“变量名_下标”:数据}
        """
        import pymysql
        from pymysql import cursors
        config = {"cursorclass": cursors.DictCursor}
        # 读取全局变量 - 根据选择的数据 读取指定的数据库配置 连接对应的数据库
        db_config = g_context().get_dict("_database")[kwargs["数据库"]]
        config.update(db_config)

        con = pymysql.connect(**config)
        cur = con.cursor()
        cur.execute(kwargs["SQL"])
        rs = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询结果:", rs)

        var_names = kwargs["引用变量"].split(",")
        result = {}
        for i, data in enumerate(rs, start=1):
            for j, value in enumerate(var_names):
                result[f'{var_names[j]}_{i}'] = data.get(var_names[j])  # 根据变量名称找读取出来的内容
        g_context().set_by_dict(result)

    # TODO: 扩展 - 文本断言方法
    @allure.step("参数数据：断言当前文本内容")
    def assert_text_comparators(self, **kwargs):
        """
        封装断言以进行不同的比较操作。

        参数:
        value (Any): 要比较的值。
        expected (Any): 预期的值。
        op_str (str): 操作符的字符串表示（如 '>', '<', '==' 等）。
        message (str, optional): 自定义的错误消息。

        返回:
        None: 如果断言成功，则不返回任何内容。

        引发:
        AssertionError: 如果断言失败。
        """
        comparators = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '==': lambda a, b: a == b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '!=': lambda a, b: a != b,
        }

        message = kwargs.get("MESSAGE", None)

        if kwargs["OP_STR"] not in comparators:
            raise ValueError(f"没有该操作方式: {kwargs['OP_STR']}")

        if not comparators[kwargs['OP_STR']](kwargs['VALUE'], kwargs["EXPECTED"]):
            if message:
                raise AssertionError(message)
            else:
                raise AssertionError(f"{kwargs['VALUE']} {kwargs['OP_STR']} {kwargs['EXPECTED']} 失败")



    # TODO: 扩展 - 全量断言-对比两个Json的差异
    @allure.step("参数数据：全量断言-对比两个Json的差异")
    def assert_json_DeepDiff(self, **kwargs):
        """
        对比两个json的差异
        :param json1: 期望结果
        :param json2: 实际结果
        :param exclude_paths:需要排除的字段，集合的类型，比如{“id”,...}
        :param ignore_order: 忽略顺序，一般用户有序数据类型，比如列表
        :param ignore_string_case:忽略值的大小写，False
        :return: 当数据没有差异则返回空集合
        """
        json1 = kwargs["json1"]
        json2 = kwargs["json2"]

        exclude_paths = kwargs.get("过滤字段", None)
        ignore_order = kwargs.get("忽略顺序", None)
        ignore_string_case = kwargs.get("忽略大小写", False)

        screen_data = {"exclude_paths": exclude_paths, "ignore_order": ignore_order,
                       "ignore_string_case": ignore_string_case}

        diff = DeepDiff(json1, json2, **screen_data)

        assert not diff, f"全量断言失败:{diff}"

    # TODO: 扩展 - 加密处理
    @allure.step("参数数据：对数据进行AES加密处理")
    def encrypt_aes(self, **kwargs):
        """
        对数据进行AES加密
        :param data: 需要加密的数据
        :param VARNAME: 存储到全局变量的名称
        :return:
        """
        key = b"1234567812345678"  # key 密码
        data = kwargs["data"].encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)  # 使用ECB模式
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))  # 使用PKCS7填充,初始化数据块大小, 16位
        encrypt_data = base64.b64encode(ct_bytes).decode('utf-8')

        g_context().set_dict(kwargs["VARNAME"], encrypt_data)  # 根据变量名设置成变量
        print("-----------------------")
        print(g_context().show_dict())
        print("-----------------------")

    # ----------------------实战扩展方法------------------------------
    @allure.step("参数数据：对数据进行AES加密处理")
    def generate_name(self, **kwargs):
        data = "hami" + str(random.randint(0, 9999))
        g_context().set_dict(kwargs["VARNAME"], data)  # 根据变量名设置成变量


    # TODO: 扩展 - JSOND断言方法
    @allure.step("参数数据：JSOND断言文本内容")
    def assert_json_comparators(self, **kwargs):
        """
        封装断言以进行不同的比较操作。

        参数:
        value (Any): 要比较的jsonPath值。
        expected (Any): 预期的值。
        op_str (str): 操作符的字符串表示（如 '>', '<', '==' 等）。
        message (str, optional): 自定义的错误消息。

        返回:
        None: 如果断言成功，则不返回任何内容。

        引发:
        AssertionError: 如果断言失败。
        """
        comparators = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '==': lambda a, b: a == b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '!=': lambda a, b: a != b,
        }

        message = kwargs.get("MESSAGE", None)

        if kwargs["OP_STR"] not in comparators:
            raise ValueError(f"没有该操作方式: {kwargs['OP_STR']}")

        # 通过jsonpath获取对应的数据
        # 获取响应数据
        response = g_context().get_dict("current_response").json()
        ex_data = jsonpath.jsonpath(response, kwargs['VALUE'])[0] # 默认就取第一个

        if not comparators[kwargs['OP_STR']](ex_data, kwargs["EXPECTED"]):
            if message:
                raise AssertionError(message)
            else:
                raise AssertionError(f"{ex_data} {kwargs['OP_STR']} {kwargs['EXPECTED']} 失败")
