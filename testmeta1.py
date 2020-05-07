class Mytype(type):
    def __init__(self,*args,**kwargs): #1.程序刚启动的时候执行,因为程序启动的时候Foo类就创建了,既然创建了,那么Mytype下的__init__就执行了
        print("创建类之前")
        super(Mytype, self).__init__(*args,**kwargs)
        print("创建类之后")

    # def __call__(cls, *args, **kwargs): #实例化的时候先执行mytype的call方法,为什么? 因为Foo是由Mytype创建的类也就是对象,加括号后,会执行Mytype类的__call__方法
    #     print("{}.__call__".format(cls.__class__.__name__))
    #     print("Mytype:new")
    #     obj=cls.__new__(cls,*args,**kwargs)
    #     print("Mytype:init")
    #     cls.__init__(obj,*args,**kwargs)
    #     return obj

class Foo(object,metaclass=Mytype): #当前类是由type类创建,metaclass可以指定当前类是由哪个type创建的
   # __metaclsss__=type #python 2的写法
    city='北京'
    def __init__(self,name):
        print("{}.__init__".format(self.__class__.__name__))
        self.name=name
    def __new__(cls, *args, **kwargs):
        print("{}.__new__".format(cls.__name__))
        return object.__new__(cls)
    def func(self,x):
        return x+1



print('========================================')
f=Foo("小红")