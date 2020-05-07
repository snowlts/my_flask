class GenericAlias:
    def __init__(self, origin, item):
        self.origin = origin
        self.item = item
    def __mro_entries__(self, bases):
        return (self.origin,)

class NewList:
    def __class_getitem__(cls, item):
        return GenericAlias(cls, item)

class Tokens(NewList[int]):
    ...

print(NewList[int])
print(dir(NewList[int]))
print(NewList[int].__mro_entries__(NewList[int]))
type(NewList[int])

print(Tokens.__bases__)
print(Tokens.__orig_bases__)
print(Tokens.__mro__)

# assert Tokens.__bases__ == (NewList,)
# assert Tokens.__orig_bases__ == (NewList[int],)
# assert Tokens.__mro__ == (Tokens, NewList, object)