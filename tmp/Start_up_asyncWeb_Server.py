from twisted.web import server, resource
from twisted.internet import reactor

class HelloResource(resource.Resource):
    isLeaf = True
    numberRequests = 0
    
    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        return "You want to send to Kannel : http://" + str(request)[59:69].split('&')[0] + str(request.uri) + "\n"

reactor.listenTCP(8080, server.Site(HelloResource()))
reactor.run()
