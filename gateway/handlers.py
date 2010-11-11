#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8

import transaction
import simplejson
from webob import Response
from webob.exc import HTTPFound
from pyramid.view import action
from gateway.models import DBSession, Meter, Message, Circuit, \
    PrimaryLog, Job

breadcrumbs = [{ "text" : "Manage Home", "url" : "/" }] 

class Dashboard(object):
    """
    Home page for the gateway
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = list(breadcrumbs)

    @action(renderer='index.mako')
    def index(self):
        session  = DBSession()  
        meters = session.query(Meter)
        return {"meters" :  meters, "breadcrumbs" : self.breadcrumbs} 

class MetersHandler(object):
    """
    """
    
    def __init__(self,request):
        self.request = request
        self.breadcrumbs = list(breadcrumbs) 

    @action(renderer="meter/add.mako") 
    def add(self): 
        session  = DBSession()  
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append({"text" : "Add a new meter"})
        if self.request.method == "POST": 
            params = self.request.params
            meter = Meter(name=params.get("name"),
                          location=params.get("location"),
                          battery=params.get("battery"),)
            session.add(meter)
            return HTTPFound(
                location="%s%s" % (self.request.application_url,
                                   meter.url()))
        else: 
            return {"breadcrumbs": self.breadcrumbs} 


class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters 
    """    
    def __init__(self,request):
        self.request = request
        session  = DBSession()  
        self.meter = session.query(Meter).filter_by(
            uuid=self.request.matchdict["id"]).one()
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="meter/index.mako") 
    def index(self):       
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text" : "Meter Overview"})
        return { "meter" : self.meter, 
                 "breadcrumbs" : breadcrumbs } 
    
    @action()
    def get_circuits(self):
        session  = DBSession()  
        return Response(
            content_type="application/json",
            body=simplejson.dumps(
                [x.toJSON() for x in session.query(
                        Circuit).filter_by(meter=self.meter.id)])) 

    @action(request_method='POST')
    def add_circuit(self): 
        session  = DBSession()  
        params = self.request.params
        circuit = Circuit(meter=self.meter.id,
                          ip_address=params.get("ip_address"),
                          energy_max=params.get("energy_max"),
                          power_max=params.get("power_max"))
        session.add(circuit)                
        return Response(
            content_type="application/json",
            body=simplejson.dumps(circuit.toJSON()))
  

    @action(renderer="meter/edit.mako")
    def edit(self): 
        return { "meter" : self.meter } 
            
    @action() 
    def remove(self): 
        session  = DBSession()  
        session.delete(self.meter)        
        [session.delete(x) 
         for x in session.query(Circuit).filter_by(meter=self.meter.id)] 
        transaction.commit()
        return HTTPFound(location="/")

class CircuitHandler(object):
    
    def __init__(self,request ):
        session = DBSession() 
        self.request = request
        self.circuit = session.query(Circuit).filter_by(
            uuid=self.request.matchdict["id"]).one()
        self.meter = self.circuit.get_meter()
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="circuit/index.mako") 
    def index(self): 
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append({"text": "Meter Overview", "url" : self.meter.url()})
        breadcrumbs.append({"text" : "Circuit Overview"}) 
        return { "breadcrumbs" : breadcrumbs,
                 "circuit" : self.circuit } 

    @action(renderer="circuit/edit.mako")
    def edit(self): 
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append(
            {"text": "Meter Overview", "url" : self.meter.url()})
        breadcrumbs.append(
            {"text" : "Circuit Overview", "url" : self.circuit.url()}) 
        breadcrumbs.append({"text" : "Circuit Edit",}) 
        return { "breadcrumbs" : breadcrumbs,
                 "circuit" : self.circuit } 

    @action()
    def toggle(self): 
        self.circuit.toggle_status() 
        return HTTPFound(location=self.circuit.url())
    
    @action() 
    def graph(self): 
        return Response("stuff")

    @action()
    def remove(self): 
        session = DBSession() 
        session.delete(self.circuit)
        return HTTPFound(location=self.meter.url())


class LoggingHandler(object):
    
    def __init__(self,request ):
        session = DBSession() 
        self.request = request
        matchdict = self.request.matchdict
        self.meter = session.\
            query(Meter).filter_by(name=matchdict["meter"]).first()
        self.circuit = session.\
            query(Circuit).filter_by(ip_address=matchdict["circuit"]).first() 

                
    @action()
    def pp(self): 
        params = self.request.params
        session = DBSession() 
        if not self.meter or not self.circuit: 
            return Response(status=404)
        log = PrimaryLog(circuit=self.circuit,
                   watthours=params["wh"],
                   use_time=params["tu"],
                   credit=params["cr"],
                   status=params["status"],
                   time=params["ts"]) 
        session.add(log) 
        return Response("ok") 

    @action()
    def sp(self): 
        return Response(self.request) 

class JobHandler(object):
    
    def __init__(self,request):
        self.request = request

    def _get_jobs(self,circuits): 
        session = DBSession() 
        l = [] 
        for circuit in circuits: 
            [l.append(x.toString()) 
             for x in session.query(Job).\
                 filter_by(circuit=circuit)]
        return l

    @action() 
    def meter(self): 
        session = DBSession() 
        matchdict = self.request.matchdict
        meter = session.query(Meter).filter_by(name=matchdict["id"]).first()
        circuits = list(session.query(Circuit).filter_by(meter=meter.id))
        return Response(self._get_jobs(circuits))
        
    @action() 
    def job(self): # bad name because of legacy code 
        return Response() 

class AlertHandler(object):
    """
    Handles all of the alert from the meter.
    Often sends a SMS message as a result
    """
    def __init__(self,request ):
        self.request = request
        
    @action() 
    def md(self): 
        """
        Meter down
        """
        return Response() 
    
    @action() 
    def sdc(self): 
        """
        """
        return Response() 
        
    @action()
    def lcw(self): 
        """
        Low credit alert
        """
        return Response()

    @action() 
    def nocw(): 
        """
        No credit alert 
        """
        return Response() 


class SMSHandler(object):    
    
    def __init__(self,request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:] 

    @action(renderer="sms/index.mako") 
    def index(self):
        session  = DBSession()  
        msgs = session.query(Message).all()
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text" : "SMS Message"})
        return { "msgs" : msgs,
                 "breadcrumbs" : breadcrumbs } 

    @action() 
    def send(self):
        session  = DBSession()  
        msgJson = simplejson.loads(self.request.body)
        message = Message(
            uuid=msgJson["uuid"],
            incoming=True,
            sent=False,
            text=msgJson["text"],
            origin=msgJson["from"])
        session.add(message) 
        return Response() 

    @action() 
    def received(self): 
        session = DBSession() 
        return Response(
            content_type="application/json",                        
            body=[x.toJSON() for x in session.\
                      query(Message).filter_by(incoming=False).\
                      filter_by(sent=False)]) 
