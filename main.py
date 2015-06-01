from cgi import parse_qs, escape
import urllib2, json
import tmdbsimple as tmdb

def getJson():
    url = "http://www.bbc.co.uk/tv/programmes/formats/films/player/episodes.json"
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return data

def getMovies(jsonData):
    episodes = jsonData['episodes']
    titles = list()
    for episode in episodes:
        titles.append(episode['programme']['title'])
    return titles

def getRatings(titles):
    tmdb.API_KEY = '1e0efd228aa91dd23e78d086c30ad1e6'
    search = tmdb.Search()
    result = dict()
    for title in titles:
        response = search.movie(query=title)
        result[title] = response['results'][0]['vote_average']
    return result

def formatData(data):
    html = "<html>"
    for title in data:
        html += "<h2>"
        html += json.dumps(title)[1:-1]
        html += "</h2>"
        html += "<h3>"
        html += json.dumps(data[title])
        html += "</h3>"
    html += "</html>"
    return html


def main(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    jsonData = getJson()
    titles = getMovies(jsonData)
    data = getRatings(titles)
    data = formatData(data)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [data]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8081,main)
    srv.serve_forever()
