#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: metaclass
# Date: 3/13/2019
"""
元类实例
"""


# 在元类中控制把自定义类的数据属性都变成大写
class UpperAttrNameMetaClass(type):  # 1. 要继承元类type，继承type的属性
    # 控制新类的创建
    def __new__(cls, clsname, bases, attrdict, *args, **kwargs):  # 2. 参数都是从type.__call__传递过来的。
        print('1. 创建新类型')
        new_attrs = dict()
        for attr, value in attrdict.items():  # 这里是将所有普通属性名变大写
            if not callable(value) and not str(attr).startswith('__'):
                new_attrs[attr.upper()] = value
            else:
                new_attrs[attr] = value

        cls_obj = super().__new__(cls, clsname, bases, new_attrs, *args, **kwargs)  # 3. 通过type创建一个新类。
        # 实际就是调用type()
        return cls_obj

    def __init__(self, clsname, bases, attrdict):  # 这里的初始化的调用实在type.__call__ 是在调用上面的__new__后调用的，
        # 参数也会传递
        self.test = 'test'  # 给创建的新类，添加一个类属性。
        print('2. 初始化新类型，增加test属性', clsname, bases, attrdict)

    def __call__(self, *args, **kwargs):  # 4. 控制新类的实例化行为
        print('3. 进行新类的实例化行为')
        # new_obj = object.__new__(self)  # __call__方法不创建对象，是调用self的__new__方法，容易在这里创建对象
        new_obj = self.__new__(self, *args, **kwargs)  # 这里的self就是一个类对象，而__new__方法的第一个参数都是类，所以也是self传入。
        # 方式一：
        self.__init__(new_obj, *args, **kwargs)
        # 方式二：
        # new_obj.__init__(*args, **kwargs)

        return new_obj  # 5. 必须返回新创建的对象


if __name__ == '__main__':
    # 测试UpperAttrNameMetaClass
    class Pig(metaclass=UpperAttrNameMetaClass):
        size = 'Big'

        def __new__(cls, *args, **kwargs):
            print('4. 元类的')
            obj = object.__new__(cls)  # 创建一个实例对象
            return obj

        def __init__(self):
            self.name = '佩奇'

        def talk(self):
            print(self.name)


    print(Pig.__dict__)
