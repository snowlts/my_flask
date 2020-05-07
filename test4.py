class MyList:
    def __getitem__(self, index):
        return index + 1
    def __class_getitem__(cls, item):
        return f"{cls.__name__}[{item.__name__}]"

class MyOtherList(MyList):
    pass


print(MyList()[0])
print(MyList[int] )
assert MyList()[0] == 1
assert MyList[int] == "MyList[int]"

print(MyOtherList()[0])
print(MyOtherList[int])
assert MyOtherList()[0] == 1
assert MyOtherList[int] == "MyOtherList[int]"