import transaction
from webob import Response
from webob.exc import HTTPFound
from pyramid.view import action
from pyramid.url import route_url

from gateway.models import DBSession, Meter
session  = DBSession()  

class Dashboard(object):
    """
    Home page for the gateway
    """
    def __init__(self, request):
        self.request = request

    @action(renderer='index.mako')
    def index(self):
        meters = session.query(Meter)
        return dict(
            meters=meters)

    @action() 
    def edit(self): 
        return Response("stuff")

class MetersHandler(object):
    """
    """
    
    def __init__(self,request):
        self.request = request
        
    @action(renderer="meter/add.mako") 
    def add(self): 
        if self.request.method == "POST": 
            name = self.request.params.get("name") 
            location = self.request.params.get("location") 
            meter = Meter(name=name,location=location) 
            session.add(meter) 
            transaction.commit()
            return HTTPFound(location="/") 
        else : 
            return {} 


class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters 
    """    
    def __init__(self,request):
        self.request = request
        self.meter = session.query(Meter).get(int(self.request.matchdict["id"]))

    @action(renderer="meter/index.mako") 
    def index(self):         
        return { "meter" : self.meter } 
        
    @action(renderer="meter/edit.mako")
    def edit(self): 
        return { "meter" : self.meter } 
            
    @action(renderer="meter/remove.mako") 
    def remove(self): 
        return { "meter" : self.meter } 
