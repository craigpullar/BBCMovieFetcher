from cgi import parse_qs, escape





def main(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    style = "<style>h1 {color:blue;}</style>"
    subject = "<h1>Hello World<h1>"
    subject = style + subject
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [subject]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080,main)
    srv.serve_forever()
