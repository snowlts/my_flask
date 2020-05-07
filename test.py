# # import time
# # import threading
# #
# # # local = threading.local()
# # local=0
# #
# # def func(n):
# #     global local
# #     local.value = n
# #     time.sleep(3)
# #     print(threading.current_thread().name,local.value)
# #
# # for i in range(5):
# #     t = threading.Thread(target=func,args=(i,),name='Thread %d' % i)
# #     t.start()
#
# # from wsgiref.simple_server import make_server
# # from hello import application
# #
# #
# # httpd = make_server('', 8000, application)
# # print('Serving http on port 8000')
# # httpd.serve_forever()
#
# from flask import Flask,request,session,g,current_app
#
# app = Flask('__name__')
#
# from werkzeug.wrappers import Request,Response
#
# def application(environ,start_response):
#     request = Request(environ)
#     response=Response('Hello, %s' % request.args.get('name','World'))
#     return response(environ,start_response)
#
# if __name__ == '__main__':
#     from werkzeug import run_simple
#     run_simple('localhost',8000,application)
#
#
# from werkzeug.local import Local, LocalManager
#
# local = Local()
# local_manager = LocalManager([local])
#
# def application(environ, start_response):
#     local.request = request = Request(environ)
#     ...
#
# application = local_manager.make_middleware(application)



# from werkzeug.wrappers import Request,Response
#
# def application(environ,start_response):


class metaA(type):
    def __init__(cls,name,bases,dict):
        super().__init__(name,bases,dict)


# type()


#
#
# print(type(C))
# print(C.__mro__)

# print(type(B))
# print(B.__mro__)

print(type(metaA))
print(metaA.__mro__)

class B:
    pass

# print(B.__name__,B.__bases__,dict(B.__dict__))
B = metaA(B.__name__,B.__bases__,dict(B.__dict__))
print(type(B))
print(B.__mro__)


class C(B):
    pass

print(type(C))
print(C.__mro__)


