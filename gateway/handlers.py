import transaction
from webob import Response
from pyramid.view import action

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

        
class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters 
    """    
    def __init__(self,request):
        self.request = request
        self.meter = session.query(Meter).filter_by(
            id=self.request.matchdict["id"]).one()

    @action(renderer="meter.mako") 
    def index(self):         
        return { "meter" : self.meter } 
        
    @action()
    def edit(self): 
        return Response("edit this meter %s" % self.meter) 
            
    @action() 
    def remove(self): 
        return Response("removed meter") 
