import transaction
import random
import uuid 
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Unicode, DateTime,\
    ForeignKey, String, Float, Boolean,Numeric
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker, relation
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Allow
from pyramid.security import Everyone


DBSession = scoped_session (sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:admins', 'admin') ]
    def __init__(self, request):
        pass

def get_now(): 
    return datetime.datetime.now()

class Meter(Base):
    """
    A table that repsents a meter in the gateway
    """
    __tablename__ = "meter"
    
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    name = Column(Unicode(255), unique=True) 
    location = Column(String)
    status = Column(Boolean) 
    date = Column(DateTime) 
    battery = Column(Integer) 
    panel_capacity = Column(Integer) 
    
    def __init__(self,name,location,battery):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.location = location 
        self.status = False 
        self.date = get_now() 
        self.battery = battery

    def get_circuits(self): 
        session = DBSession() 
        return [x for x in session.\
                    query(Circuit).filter_by(meter=self)] 

    def url(self): 
        return "/meter/index/%s" % self.uuid 

    def edit_url(self): 
        return "/meter/edit/%s" % self.uuid
   
    def remove_url(self): 
        return "meter/remove/%s" % self.uuid

    def __str__(self): 
        return "<Meter %s>" % self.uuid

class Account(Base):
    """
    """
    __tablename__ = "account" 
    id = Column(Integer, primary_key=True)
    pin = Column(String)
    name = Column(String)
    phone = Column(String)
    lang = Column(String)

    def __init__(self,name="default",phone=None,lang="en"):
        self.name = name
        self.phone = phone
        self.lang = lang

    def url(self): 
        return "account/index/%s" % self.id


class Circuit(Base):
    """
    """
    __tablename__ = "circuit" 
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    date = Column(DateTime) 
    pin = Column(String) 
    meter_id = Column("meter",ForeignKey("meter.id"))
    meter  = relation(Meter, primaryjoin=meter_id == Meter.id)
    energy_max = Column(Float)
    power_max = Column(Float)
    status = Column(Integer) 
    ip_address = Column(String) 
    credit = Column(Float) 
    account_id  = Column(Integer, ForeignKey('account.id'))
    account  = relation(Account, primaryjoin=account_id == Account.id)



    def __init__(self,meter,account,
                 energy_max,power_max,ip_address,status=1,credit=0):
        self.date = get_now()
        self.uuid = str(uuid.uuid4())
        self.pin = self.get_pin()
        self.meter = meter 
        self.energy_max = energy_max
        self.power_max = power_max
        self.ip_address = ip_address
        self.status = status
        self.credit = credit
        self.account = account

    def get_pin(self): 
        chars = "qwertyuipasdfghjkzxcvbnm"
        ints = "23456789" 
        return "%s%s" % ("".join(random.sample(chars,3)),
                      "".join(random.sample(ints,3)))

    def get_jobs(self):
        session = DBSession()
        return session.query(Job).\
            filter_by(circuit=self).order_by(Job.id.desc())

    def get_logs(self): 
        session = DBSession() 
        return session.query(PrimaryLog).\
            filter_by(circuit=self).order_by(PrimaryLog.id.desc())

    def toggle_status(self): 
        session = DBSession() 
        if self.status == 0: 
            job = TurnOn(circuit=self)
            session.add(job)
        else:             
            job = TurnOff(circuit=self) 
            session.add(job)

    def url(self): 
        return "/circuit/index/%s" % self.uuid

    def edit_url(self): 
        return "/circuit/edit/%s" % self.uuid 

    def remove_url(self): 
        return "/circuit/remove/%s" % self.uuid 
    
    def toggle_url(self): 
        return "/circuit/toggle/%s" % self.uuid

    def toJSON(self): 
        return { "id" : self.id,
                 "ip_address" : self.ip_address,
                 "date" : str(self.date),
                 "url" : self.url(),
                 "pin" : self.pin,
                 "uuid" : self.uuid,
                 "energy_max" : self.energy_max,
                 "power_max" : self.power_max, 
                 "status" : self.status } 

class Message(Base):
    """
    """
    __tablename__  = "sms_message" 
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    uuid = Column(String) 
    incoming = Column(Boolean) 
    sent = Column(Boolean) 
    text = Column(String) 
    to = Column(Numeric) 
    origin = Column(Numeric)
    
    def __init__(self,uuid,incoming,sent,text,origin=1,to=1):
        self.date = get_now() 
        self.uuid = uuid
        self.incoming = incoming
        self.sent = sent 
        self.text = text 
        self.to = to 
        self.origin = origin 

    def url(self): 
        return "sms/message" 

    def toDict(self): 
        return { "from" : int(self.origin),
                 "time" : str(self.date),
                 "to"   : int(self.to),
                 "uuid" : self.uuid,
                 "text" : self.text,
                 "id"   : self.id, } 

    @staticmethod
    def send_message(to=None,text=None): 
        session = DBSession() 
        session.add(Message(
                uuid=str(uuid.uuid4()),
                incoming=False,
                sent=False,
                text=text,
                to=to))
        transaction.commit()

    def __unicode__(self): 
        return "Messsage <%s>" % self.uuid

class TokenBatch(Base): 
    __tablename__ = "tokenbatch"
    id = Column(Integer, primary_key=True)    
    uuid = Column(String)
    created = Column(DateTime)
    
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.created = datetime.datetime.now()
    
    def url(self): 
        return "token/batch/%s" % self.uuid

    def get_tokens(self): 
        session = DBSession()
        return session.query(Token).filter_by(batch=self)

class Token(Base):
    __tablename__  = "token" 

    id = Column(Integer, primary_key=True)    
    created = Column(DateTime) 
    token = Column(Numeric) 
    value = Column(Numeric) 
    state = Column(String)
    batch_id = Column(Integer, ForeignKey('tokenbatch.id'))
    batch  = relation(TokenBatch, primaryjoin=batch_id == TokenBatch.id)

    def __init__(self,token,batch,value,state="new"):
        self.created = datetime.datetime.now()
        self.token = token
        self.value = value
        self.state = state
        self.batch = batch 

    @staticmethod
    def get_random():     
        r =  int(random.random() * 10**11)
        if r > 10**10: return r 
        else: return Token.get_random() 

    def toDict(self): 
        return { 
            "id" : self.id,
            "state" : self.state,
            "value" : int(self.value),
            "token" : int(self.token),
            "created" : self.created.ctime()} 
        

class Log(Base): # really a circuit log 
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    uuid = Column(String) 
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit, primaryjoin=circuit_id == Circuit.id)
    
    
    def __init__(self,circuit): 
        self.date = get_now() 
        self.uuid = str(uuid.uuid4())
        self.circuit = circuit

class SystemLog(Base): # to mark system errors
    __tablename__ = "system_log" 
    id = Column(Integer, primary_key=True)
    uuid = Column(String) 
    text = Column(String) 
    created = Column(String) 

    def __init__(self,text):
        self.uuid = str(uuid.uuid4())
        self.text = text
        self.created = get_now() 
        


class PrimaryLog(Log): 
    __tablename__ = "primary_log" 
    __mapper_args__ = {'polymorphic_identity': 'primary_log'}
    id = Column(Integer, ForeignKey('log.id'), primary_key=True)
    watthours = Column(Float) 
    use_time = Column(Float) 
    status = Column(Integer) 
    created = Column(String) 
    credit = Column(Float) 
    status = Column(Integer) 

    def __init__(self,circuit,credit,watthours,use_time,status):
        Log.__init__(self,circuit)
        self.circuit = circuit
        self.watthours = watthours
        self.use_time = use_time 
        self.credit = credit
        self.created = get_now()
        self.status = status
    

class Job(Base):
    __tablename__ = "jobs" 
    id = Column(Integer, primary_key=True)
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    uuid  = Column(String) 
    start = Column(String) 
    end = Column(String)
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit, primaryjoin=circuit_id == Circuit.id)
    state = Column(Boolean)

    def __init__(self,circuit,state=True): 
        self.uuid = str(uuid.uuid4())
        self.start = get_now() 
        self.circuit = circuit
        self.state = state 

    def url(self): 
        return "jobs/job/%s/" % self.id

    def toJSON(self): 
        return {"uuid": self.uuid,
                "state" : self.state,
                "date": self.start,
                "type": self._type} 

class AddCredit(Job):
    __tablename__ = "addcredit" 
    __mapper_args__ = {'polymorphic_identity': 'addcredit'}
    description = "This job adds energy credit to the remote circuit"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    credit = Column(Integer)     

    def __init__(self,credit,circuit): 
        Job.__init__(self,circuit)
        self.credit = credit 
        
    def toString(self): 
        return "job=cr&jobid=%s&cid=%s&amt=%s;" % (self.id,
                                                self.circuit.ip_address,
                                                self.credit)

class TurnOff(Job):
    __tablename__ = "turnoff" 
    __mapper_args__ = {'polymorphic_identity': 'turnoff'}
    description = "This job turns off the circuit on the remote meter"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self,circuit): 
        Job.__init__(self,circuit=circuit) 

    def toString(self): 
        return "job=coff&jobid=%s&cid=%s;" % (self.id,self.circuit.ip_address)
        
class TurnOn(Job):
    __tablename__ = "turnon"
    __mapper_args__ = {'polymorphic_identity': 'turnon'}
    description = "This job turns on the circuit off the remote meter"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    
    def __init__(self,circuit): 
        Job.__init__(self,circuit=circuit) 

    def toString(self): 
        return "job=con&jobid=%s&cid=%s;" % (self.id,self.circuit.ip_address)
        


        
def populate():
    DBSession.flush()
    transaction.commit()


def initialize_sql(db_string, db_echo=False):
    engine = create_engine(db_string, echo=db_echo)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        pass
