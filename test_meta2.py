class Singleton(type):
    def __init__(cls,*args,**kwargs):
        cls.__instance = None
        super().__init__(*args,**kwargs)

    def __call__(cls, *args, **kwargs):

        if cls.__instance is None:
            print('call1')
            cls.__instance = super().__call__(*args,**kwargs)
            return cls.__instance
        else:
            print('call2')
            return cls.__instance


class Spam(metaclass=Singleton):
    def __init__(self):
        print("Creating Spam")


a=Spam()
b=Spam()
c=Spam()
print(a,b)