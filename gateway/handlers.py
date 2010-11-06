import transaction
from webob import Response

from pyramid.view import action
from gateway.models import DBSession, Meter

class Dashboard(object):
    """
    Home page for the gateway
    """
    def __init__(self, request):
        self.request = request

    @action(renderer='index.mako')
    def index(self):
        session  = DBSession()  
        meters = session.query(Meter)
        return dict(meters=meters)

    @action() 
    def edit(self): 
        return Response("stuff")


class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters 
    """    
    def __init__(self,request):
        self.request = request
        
    @action() 
    def index(self): 
        return Response() 
    
    @action() 
    def add(self): 
        return Response() 
    
    @action()
    def edit(self): 
        return Response() 
            
    @action() 
    def remove(self): 
        return Response() 
