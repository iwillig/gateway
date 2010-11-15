import datetime
import simplejson
from urlparse import parse_qs 
from webob import Response
from webob.exc import HTTPFound
from pyramid.view import action
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget
from gateway.models import DBSession, Meter, Message, Circuit, \
    PrimaryLog, Job, AddCredit, Account, TokenBatch, Token
from gateway.messaging import sendMessageQueue
from gateway.security import USERS

breadcrumbs = [{ "text" : "Manage Home", "url" : "/" }] 

class Dashboard(object):
    """
    Home page for the gateway
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    @action(renderer='index.mako',permission="view")
    def index(self):
        meters = self.session.query(Meter)
        tokenBatchs = self.session.query(TokenBatch).all() 
        return {
            "logged_in" : authenticated_userid(self.request),
            "tokenBatchs" : tokenBatchs,
            "meters" :  meters, 
            "breadcrumbs" : self.breadcrumbs} 

    @action(renderer="meter/add.mako",permission="admin") 
    def add_meter(self): 
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append({"text" : "Add a new meter"})
        if self.request.method == "POST": 
            params = self.request.params
            meter = Meter(name=params.get("name"),
                          location=params.get("location"),
                          battery=params.get("battery"),)
            self.session.add(meter)
            return HTTPFound(
                 location="%s%s" % (self.request.application_url,
                                    meter.url()))

        else: 
            return {
                "logged_in" : authenticated_userid(self.request),
                "breadcrumbs": self.breadcrumbs} 

    @action(permission="admin")
    def add_tokens(self): 
        self.request.params
        batch =  TokenBatch() 
        self.session.add(batch)
        for number in xrange(0,int(self.request.params["amount"])):
            self.session.add(Token(
                    token=Token.get_random(),
                    value = self.request.params["value"],
                    batch = batch))
        return HTTPFound(location=self.request.application_url)

class UserHandler(object):
    
    def __init__(self,request ):
        self.request = request
        
    @action(renderer="login.mako")
    def login(self): 
        came_from = self.request.params.get('came_from',)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in self.request.params:
              login = self.request.params['login']
              password = self.request.params['password']
              if USERS.get(login) == password:
                  headers = remember(self.request, login)
                  return HTTPFound(location = "/",
                                   headers = headers)
              message = 'Failed login' 
        return dict(
            message = message,
            url = self.request.application_url + '/login',
            came_from = came_from,
            login = login,
            password = password,
            )

    def logout(self): 
        headers = forget(self.request)
        return HTTPFound(
            headers = headers,
            location=self.request.application_url)
        


class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters 
    """    
    def __init__(self,request):
        self.request = request
        self.session  = DBSession()  
        self.meter = self.session.query(Meter).filter_by(
            uuid=self.request.matchdict["id"]).one()
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="meter/index.mako",permission="admin") 
    def index(self):       
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text" : "Meter Overview"})
        return { 
            "logged_in" : authenticated_userid(self.request),
            "meter" : self.meter, 
            "breadcrumbs" : breadcrumbs } 
    
    @action()
    def get_circuits(self):
        session  = DBSession()  
        return Response(
            content_type="application/json",
            body=simplejson.dumps(
                [x.toJSON() for x in session.query(
                        Circuit).filter_by(meter=self.meter)])) 

    @action(request_method='POST',permission="admin")
    def add_circuit(self): 
        params = self.request.params
        account = Account(phone=params.get("phone"))
        circuit = Circuit(meter=self.meter,
                          account=account,
                          ip_address=params.get("ip_address"),
                          energy_max=params.get("energy_max"),
                          power_max=params.get("power_max"))
        self.session.add(account)
        self.session.add(circuit)                
        return Response(
            content_type="application/json",
            body=simplejson.dumps(circuit.toJSON()))
  

    @action(renderer="meter/edit.mako",permission="admin")
    def edit(self): 
        return { "meter" : self.meter } 
            
    @action(permission="admin") 
    def remove(self): 
        self.session.delete(self.meter)        
        [self.session.delete(x) 
         for x in self.session.query(Circuit).filter_by(meter=self.meter)] 
        return HTTPFound(location="/")

class CircuitHandler(object):
    
    def __init__(self,request):
        self.session = DBSession() 
        self.request = request
        self.circuit = self.session.query(Circuit).filter_by(
            uuid=self.request.matchdict["id"]).one()
        self.meter = self.circuit.meter
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="circuit/index.mako",permission="admin") 
    def index(self): 
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append({"text": "Meter Overview", "url" : self.meter.url()})
        breadcrumbs.append({"text" : "Circuit Overview"}) 
        return { 
            "logged_in" : authenticated_userid(self.request),
            "breadcrumbs" : breadcrumbs,                 
            "jobs" : self.circuit.get_jobs(),
            "circuit" : self.circuit } 

    @action(renderer="circuit/edit.mako",permission="admin")
    def edit(self): 
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append(
            {"text": "Meter Overview", "url" : self.meter.url()})
        breadcrumbs.append(
            {"text" : "Circuit Overview", "url" : self.circuit.url()}) 
        breadcrumbs.append({"text" : "Circuit Edit",}) 
        return { 
            "logged_in" : authenticated_userid(self.request),
            "breadcrumbs" : breadcrumbs,
            "circuit" : self.circuit } 

    @action(permission="admin")
    def toggle(self): 
        self.circuit.toggle_status() 
        return HTTPFound(location=self.circuit.url())
    
    @action(renderer="circuit/build_graph.mako",permission="admin") 
    def build_graph(self): 
        return {
            "logged_in" : authenticated_userid(self.request),
            "circuit" : self.circuit } 

    @action(renderer="circuit/show_graph.mako",permission="admin") 
    def show_graph(self): 
        return { "logged_in" : authenticated_userid(self.request)} 

    @action()
    def jobs(self): 
        return Response([x.toJSON() for x in self.circuit.get_jobs()])
    
    @action(permission="admin")
    def add_credit(self): 
        job = AddCredit(circuit=self.circuit,
                  credit=self.request.params.get("amount"))
        self.session.add(job)
        return HTTPFound(location=self.circuit.url())

    @action(permission="admin")
    def remove(self): 
        self.session.delete(self.circuit)
        return HTTPFound(location=self.meter.url())

class AccountHandler(object):
    """
    """
    
    def __init__(self,request ):
        self.session = DBSession
        self.request = request
        self.account = self.session.\
            query(Account).get(self.request.matchdict.get("id"))

    def index(self): 
        return Response(str(self.account))


class LoggingHandler(object):
    
    def __init__(self,request ):
        session = DBSession() 
        self.request = request
        matchdict = self.request.matchdict
        circuit_id = matchdict["circuit"].replace("_",".") 
        self.meter = session.\
            query(Meter).filter_by(name=matchdict["meter"]).first()
        self.circuit = session.\
            query(Circuit).filter_by(ip_address=circuit_id).first() 

                
    @action() # permission="admin"
    def pp(self): 
        """
        Primary log action. Should force the meter to provide authentication
        """
        params = parse_qs(self.request.body)
        session = DBSession() 
        if not self.meter or not self.circuit: 
            return Response(status=404)
        log = PrimaryLog(circuit=self.circuit,
                   watthours=params["wh"][0],
                   use_time=params["tu"][0],
                   credit=params["cr"][0],
                   status=int(params["status"][0])
                         ) 
        self.circuit.credit = log.credit 
        self.circuit.status = int(params["status"][0])  # fix 
        session.add(log) 
        session.merge(self.circuit)
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
                 filter_by(circuit=circuit).filter_by(state=True)]
        return "".join(l)

    @action() 
    def meter(self): 
        session = DBSession() 
        matchdict = self.request.matchdict
        meter = session.query(Meter).filter_by(name=matchdict["id"]).first()
        circuits = list(session.query(Circuit).filter_by(meter=meter))
        return Response(self._get_jobs(circuits))
        
    @action() 
    def job(self): 
        session = DBSession()
        job = session.query(Job).get(self.request.matchdict["id"])
        if self.request.method == "DELETE": 
            job.state = False
            job.end = datetime.datetime.now()
            session.merge(job)
            return Response(job.toString()) 
        else:
            return Response(job.toString()) 

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

class TokenHandler(object):
    
    def __init__(self,request ):
        self.request = request
        self.session = DBSession() 

    @action(permission="admin") 
    def batch(self): 
        batch = self.session.\
            query(TokenBatch).filter_by(uuid=self.request.matchdict["id"]).first()
        return Response(simplejson.dumps([x.toDict() for x in batch.get_tokens()]))


class MessageHandler(object):
    def __init__(self,request ):
        self.session = DBSession() 
        self.request = request
        self.message = self.session.\
            query(Message).filter_by(uuid=self.request.matchdict["id"]).first()

    @action()
    def index(self):
        return Response(simplejson.dumps(self.message.toDict())) 
    
    @action(request_method="POST")
    def remove(self): 
        print(self.request) 
        self.message.sent = True
        self.session.merge(self.message)
        return Response("ok") 
        
class SMSHandler(object):    
    
    def __init__(self,request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:] 
        self.session = DBSession()

    @action(renderer="sms/index.mako",permission="admin") 
    def index(self):
        incoming_msgs = self.session.query(Message).\
            filter_by(incoming=True).order_by(Message.id.desc())
        outgoing_msgs = self.session.query(Message).\
            filter_by(incoming=False).order_by(Message.id.desc())
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text" : "SMS Message"})
        return { 
            "logged_in" : authenticated_userid(self.request),
            "incoming_msgs" : incoming_msgs,
            "outgoing_msgs" : outgoing_msgs,
            "breadcrumbs" : breadcrumbs } 

    @action(permission="admin") 
    def remove_all(self): 
        [self.session.delete(msg) for msg in self.session.query(Message).all()]
        return HTTPFound(location="%s/sms/index" % self.request.application_url) 

    @action() 
    def ping(self): 
        return Response("ok") 

    @action() 
    def send(self):
        msgJson = simplejson.loads(self.request.body)
        message = Message(
            uuid=msgJson["uuid"],
            incoming=True,
            sent=False,
            text=msgJson["text"],
            origin=msgJson["from"])        
        self.session.add(message) 
        sendMessageQueue.put_nowait(message.toDict())  # parse the message
        return Response(message.uuid)

    @action() 
    def received(self): 
        return Response(
            content_type="application/json",                        
            body=simplejson.dumps([x.toDict() for x in self.session.\
                      query(Message).filter_by(incoming=False).\
                      filter_by(sent=False)])) 

