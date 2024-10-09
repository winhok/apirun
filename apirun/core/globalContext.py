# -*- coding: utf-8 -*-
# @Author : Hami

# 全局变量 --- 字典格式存储
# 内置属性--外部不可修改
# 提供对应的方法: 可以对这个属性进行修改\增加\显示

class g_context(object):  # 类继承
    _dic = {}  # 内置属性--外部不可修改

    # 提供对应的方法: 可以对这个属性进行修改\增加\显示

    # TODO 1 : 通过key去进行设置
    def set_dict(self, key, value):
        self._dic[key] = value

    # TODO 2 : 通过key去进行获取数据
    def get_dict(self, key):
        return self._dic.get(key, None)  # 如果这个key不存在,则会返回None

    # TODO 3 : 通过自字典去设置数据
    def set_by_dict(self, dic):
        self._dic.update(dic)

    # TODO 4 : 显示对应全局变量所有值
    def show_dict(self):
        return self._dic


context = g_context()
