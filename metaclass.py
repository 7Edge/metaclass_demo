#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: metaclass
# Date: 3/13/2019
"""
元类实例
"""


# 实例一：
# 在元类中控制把自定义类的数据属性都变成大写
class UpperAttrNameMetaClass(type):  # 1. 要继承元类type，继承type的属性
    # 控制新类的创建
    def __new__(cls, clsname, bases, attrdict, *args, **kwargs):  # 2. 参数都是从type.__call__传递过来的。
        print('1. 创建新类型, from UpperAttrNameMetaClass.__new__')
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
        super().__init__(clsname, bases, attrdict)
        print('2. 初始化新类型，增加test属性, from UpperAttrNameMetaClass.__init__')

    def __call__(self, *args, **kwargs):  # 4. 控制新类的实例化行为
        print('3. 进行新类的实例化行为, from UpperAttrNameMetaClass.__call__')
        # new_obj = object.__new__(self)  # __call__方法不创建对象，是调用self的__new__方法，容易在这里创建对象
        new_obj = self.__new__(self, *args, **kwargs)  # 这里的self就是一个类，而__new__方法的第一个参数都是类，所以也是self传入
        # __new__方法不可能是绑定到对象的方法，因为对象还没有怎么用对象调用绑定到对象的方法，对吧。
        # 方式一：
        # self.__init__(new_obj, *args, **kwargs)
        # 方式二：
        new_obj.__init__(*args, **kwargs)  # 两种方式都可以，一个是类调用，一个是绑定对象方式调用。

        return new_obj  # 5. 必须返回新创建的对象


# 实例二：
# 在元类中控制自定义的类无需init方法，且所有对象属性大写。
# 也就是说，然原类控制实例化行为，且必须是关键字参数为初始化参数行为，因为目标就是没有init方法。
class ObjectNoInitMetaClass(type):

    def __call__(cls, *args, **kwargs):
        if len(args):
            raise TypeError('must use keyword argument for key function')
        new_obj = cls.__new__(cls)
        for k, v in kwargs.items():
            setattr(new_obj, k.upper(), v)
        return new_obj


# 实例三
# 基于元类实现单例模式,比如数据库对象,实例化时参数都一样,就没必要重复产生对象,浪费内存
class SingleInstanceMetaClass(type):

    def __init__(self, name, bases, dic):
        self.__single_instance = None
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        if cls.__single_instance:
            return cls.__single_instance
        single_obj = cls.__new__(cls)
        single_obj.__init__(*args, **kwargs)
        cls.__single_instance = single_obj
        return single_obj


if __name__ == '__main__':
    # 测试UpperAttrNameMetaClass
    class Pig(object, metaclass=UpperAttrNameMetaClass):
        size = 'Big'

        def __new__(cls, *args, **kwargs):
            print('4. 元类的__call__中调用__new__, from Pig.__new__')
            obj = object.__new__(cls)  # 创建一个实例对象，一个类的不同对象都是通过object.__new__(类）产生的。
            return obj

        def __init__(self):
            print('5. 元类的__call__中实例化新对象后，进行对象的促使化， from Pig.__init__')
            self.name = '佩奇'

        def talk(self):
            print(self.name)


    Pig().talk()

    print(Pig.__dict__)  # 可以看到SIZE属性变为大写,如果小写调用报“AttributeError: type object 'Pig' has no attribute 'size'”
    print(Pig.SIZE)

    # 测试ObjectNoInitMetaClass
    class AnyOne(metaclass=ObjectNoInitMetaClass):
        pass


    foo = AnyOne(name='zjqi', age=28)

    print(foo.NAME, foo.AGE)
    print(foo.__dict__)

    # 测试SingleInstanceMetaClass

    class Setting(metaclass=SingleInstanceMetaClass):

        def __init__(self):
            self.db = 'mysql'
            self.port = 3306


    bar = Setting()
    bar2 = Setting()

    print(bar is bar2)
    print(bar.db, bar.port)
    bar.db = 'oracle'
    print(bar2.db, bar2.port)
