

class metaA(type):
    pass

class B(metaclass=metaA):
    pass


class C(B):
    pass

print(type(metaA))
print(metaA.__mro__)

print(type(B))
print(B.__mro__)

print(type(C))
print(C.__mro__)