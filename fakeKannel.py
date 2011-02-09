from pyramid.config import Configurator
from pyramid.response import Response
from paste.httpserver import serve

def sendMessage(request):
    print(request.params)
    return Response()


if __name__ == '__main__':
    config = Configurator()
    config.add_route('add-message',
                     '/cgi-bin/sendsms',
                     view=sendMessage)
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0',port=13001)
