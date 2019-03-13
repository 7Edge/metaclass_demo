# metaclass_demo
使用元类控制类的创建和实例化过程
> 创建了三个元类例子及演示代码，都放在metaclass.py文件中

- UpperAttrNameMetaClass 比较完整的演示了元类__new__/__init__/__call__/与 其实例的新类的__new__/__init__的关系
- ObjectNoInitMetaClass 完全通过元类__call__来控制类的实例化对象，没有定义\__init__方法
- SingleInstanceMetaClass 利用元类实现对象的单例。主要就是将单例放在类属性中，然后控制类的实例化过程来控制单例的返回。