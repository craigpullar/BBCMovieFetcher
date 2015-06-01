from cgi import parse_qs, escape
import urllib2, json


def getJson():
    url = "http://www.bbc.co.uk/tv/programmes/formats/films/player/episodes.json"
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return json.dumps(data)

def main(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    jsonData = getJson()
    style = "<style>h1 {color:blue;}</style>"
    subject = "<h1>Hello World<h1>"
    subject = style + subject
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [jsonData]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8081,main)
    srv.serve_forever()
