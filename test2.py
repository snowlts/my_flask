

class A:
    pass

a=A()
class B(a):
    pass



print(type(B))

print(B.__mro__)