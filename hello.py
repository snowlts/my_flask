


def application(environ, start_response):
    # start_response('200 OK', [('Content-Type', 'text/html')])
    # return ['<h1>Hello, web!</h1>'.encode()]
    status = "200 OK"
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    path = environ['PATH_INFO'][1:] or 'hello'
    return [b'<h1> %s </h1>' % path.encode()]