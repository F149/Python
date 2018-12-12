class SomeObject:
    def __init__(self):
        self.integer_field = 1
        self.float_field = 0.1
        self.string_field = "some string"


class EventSet:
    def __init__(self, type):
        self.type = type

class EventGet:
    def __init__(self, type):
        self.type = type

class NullHandler:
    def __init__(self, subccessor=None):
        self.__subccessor = subccessor

    def handle(self, obj, event):
        if self.__subccessor is not None:
            return self.__subccessor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == int:
            return obj.integer_field
        elif isinstance(event, EventSet) and isinstance(event.type, int):
            obj.integer_field = event.type
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == float:
            return obj.float_field
        elif isinstance(event, EventSet) and isinstance(event.type, float):
            obj.float_field = event.type
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == str:
            return obj.string_field
        elif isinstance(event, EventSet) and isinstance(event.type, str):
            obj.string_field = event.type
        else:
            return super().handle(obj, event)

obj = SomeObject()

class Chain():
    def __init__(self):
        self.handlers = IntHandler(FloatHandler(StrHandler(NullHandler())))

    def handle(self, obj, event):
        return self.handlers.handle(obj, event)

chain = Chain()

print(chain.handle(obj, EventGet(int)))
print(chain.handle(obj, EventGet(float)))
print(chain.handle(obj, EventGet(str)))
print("\n")
print(chain.handle(obj, EventSet(22)))
print(chain.handle(obj, EventSet("CCXXII")))
print(chain.handle(obj, EventGet(str)))
print(chain.handle(obj, EventSet(22.2)))
print("\n")
print(chain.handle(obj, EventGet(int)))
print(chain.handle(obj, EventGet(float)))
print(chain.handle(obj, EventGet(str)))


## Teacher solution
#E_INT, E_FLOAT, E_STR = "INT", "FLOAT", "STR"
#
#
#class EventGet:
#    def __init__(self, prop):
#        self.kind = {int:E_INT, float:E_FLOAT, str:E_STR}[prop];
#        self.prop = None;
#
#
#class EventSet:
#    def __init__(self, prop):
#        self.kind = {int:E_INT, float:E_FLOAT, str:E_STR}[type(prop)];
#        self.prop = prop;
#
#
#class NullHandler:
#    def __init__(self, successor=None):
#        self.__successor = successor
#
#    def handle(self, obj, event):
#        if self.__successor is not None:
#            return self.__successor.handle(obj, event)
#
#
#class IntHandler(NullHandler):
#    def handle(self, obj, event):
#        if event.kind == E_INT:
#            if event.prop is None:
#                return obj.integer_field
#            else:
#                obj.integer_field = event.prop;
#        else:
#            return super().handle(obj, event)
#
#
#class StrHandler(NullHandler):
#    def handle(self, obj, event):
#        if event.kind == E_STR:
#            if event.prop is None:
#                return obj.string_field
#            else:
#                obj.string_field = event.prop;
#        else:
#            return super().handle(obj, event)
#
#
#class FloatHandler(NullHandler):
#    def handle(self, obj, event):
#        if event.kind == E_FLOAT:
#            if event.prop is None:
#                return obj.float_field
#            else:
#                obj.float_field = event.prop;
#        else:
#            return super().handle(obj, event)
