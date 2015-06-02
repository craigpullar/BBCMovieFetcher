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

def styleData():
    style = """
    <link href='http://fonts.googleapis.com/css?family=Righteous' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>
    <style>
    html {
    background-color:#E8E8E8;
    }
    h1 {
    font-family: 'Righteous', cursive;
    text-align:center;
    padding:70px;
    background-color:#559e83;
    margin:0;
    color: white;
    font-size:30pt;
    }
    h2 {
    font-family: 'Raleway', sans-serif;
    text-align:center;
    padding:30px;
    background-color:#AE5A41;
    margin:0;
    color:white;
    font-weight:normal;
    }
    span {
    font-size:16;
    margin-left:10px;
    }
    </style>
    """
    return style

def formatData(data):
    html = "<html>"
    html += styleData()
    html += "<h1>FILMS</h1><hr />"
    for title in data:
        html += "<h2>"
        html += json.dumps(title)[1:-1]
        html += "<span>"
        html += json.dumps(data[title])
        html += "/10</span></h2><hr />"
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
