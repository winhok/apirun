# -*- coding: utf-8 -*-
# @Author : Hami
import json

# 变量渲染
# 字符串模板进行参数渲染
# 使用 jinja2 模板引擎 (类似 flask的模板)
# https://docs.jinkan.org/docs/jinja2/templates.html

from jinja2 import Template


def refresh(target, context):
    """
    把你初始数据中需要渲染的数据变成context当中的值
    :param target: 你的初始数据，用 {{变量名}} -- 请求数据
    :param context: 你的初始数据渲染的值 -- 全局变量
    :return:
    """
    if target is None: return None
    s = Template(str(target)).render(context)
    return Template(str(target)).render(context)


# 测试方法
# def t_Refresh():
#     target = "hello {{name}}, {{niasd}},{{token}}"
#     context = {"name": "张三", "token": [
# 				{
# 					"type": "套餐",
# 					"value": "套餐二"
# 				},
# 				{
# 					"type": "颜色",
# 					"value": "银色"
# 				},
# 				{
# 					"type": "容量",
# 					"value": "64G"
# 				}
# 			]}
#     res = refresh(target, context)
#     print(res)
# t_Refresh()


# data = "{'关键字': 'request_post_row_json', 'URL': 'http://shop-xo.hctestedu.com', 'PARAMS': {'s': 'api/cart/save', 'application': 'app', 'application_client_type': 'weixin', 'token': 'daf267bdf9c5a028adf6ec972ceb0bf5'}, 'DATA': {'goods_id': '2', 'spec': '[{'type': '套餐', 'value': '套餐二'}, {'type': '颜色', 'value': '银色'}, {'type': '容量', 'value': '64G'}]', 'stock': '1'}}"
# print(json.dumps(data))

