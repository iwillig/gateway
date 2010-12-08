import transaction
import random
import uuid 
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime,\
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
    phone = Column(String) 
    name = Column(String) 
    location = Column(String)
    status = Column(Boolean) 
    date = Column(DateTime) 
    battery = Column(Integer) 
    panel_capacity = Column(Integer) 
    communication = Column(String) # sms or http 
    
    def __init__(self,name,phone,location,battery,
                 panel_capacity,communication="sms"):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.phone = phone
        self.location = location 
        self.status = False 
        self.date = get_now() 
        self.battery = battery
        self.panel_capacity = panel_capacity
        self.communication = communication

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

    def __init__(self,meter,account,pin,
                 energy_max,power_max,ip_address,status=1,credit=0):
        self.date = get_now()
        self.uuid = str(uuid.uuid4())
        self.pin = pin
        self.meter = meter 
        self.energy_max = energy_max
        self.power_max = power_max
        self.ip_address = ip_address
        self.status = status
        self.credit = credit
        self.account = account

    @staticmethod
    def get_pin(): 
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

    def get_rich_status(self): 
        if self.status == 0: 
            return "Off"
        elif self.status == 1:
            return "On"
            
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
    Abstract class for all messages 
    """
    __tablename__  = "message" 
    type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': type}
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sent = Column(Boolean) 
    number = Column(String) 
    uuid = Column(String)

    def __init__(self,number,uuid,sent=False):
        self.date = get_now() 
        self.sent = sent 
        self.number = number
        self.uuid = uuid 

    def url(self): 
        return "message/index/%s" % self.uuid 

    def toDict(self): 
        return { "number" : int(self.number),
                 "time" : str(self.date),
                 "uuid" : self.uuid,
                 "text" : self.text,
                 "id"   : self.id, } 

    def __unicode__(self): 
        return "Messsage <%s>" % self.uuid

    def respond(self): 
        return 

class IncomingMessage(Message):
    """
    A class that repsents an incoming message
    """
    __tablename__ = "incoming_message" 
    __mapper_args__ = {'polymorphic_identity': 'incoming_message'}
    id = Column(Integer,ForeignKey('message.id'), primary_key=True)
    text = Column(String)

    def __init__(self,number,text,uuid,sent=True):
        Message.__init__(self,number,uuid)
        self.text = text
        
class OutgoingMessage(Message):
    """ 
    A class that repents an outgoing sms message
    """
    __tablename__ = "outgoing_message" 
    __mapper_args__ = {'polymorphic_identity': 'outgoing_message'}
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    text = Column(String) 
    incoming = Column(String,nullable=True) 

    def __init__(self,number,text,incoming=None):
        Message.__init__(self,number,str(uuid.uuid4())) 
        self.text = text 
        self.incoming = incoming

    def get_incoming(self): 
        session = DBSession() 
        incoming = session.query(IncomingMessage).\
            filter_by(uuid=self.incoming).first()
        if incoming:
            return incoming.text
        else: 
            return "message not based on incoming message"

class TokenBatch(Base): 
    __tablename__ = "tokenbatch"
    id = Column(Integer, primary_key=True)    
    uuid = Column(String)
    created = Column(DateTime)
    
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.created = datetime.datetime.now()
    
    def url(self): 
        return "token/show_batch/%s" % self.uuid

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
        
class Alert(Base): 
    __tablename__ = 'alert' 
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(String)
    message_id = Column(Integer,ForeignKey('message.id'))
    message = relation(Message,primaryjoin=message_id == Message.id) 
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit, primaryjoin=circuit_id == Circuit.id)
    
    def __init__(self,text,circuit,message): 
        self.date = get_now()
        self.circuit = circuit
        self.message = message

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
        
class SystemAlert(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        
        


class PrimaryLog(Log): 
    __tablename__ = "primary_log" 
    __mapper_args__ = {'polymorphic_identity': 'primary_log'}
    id = Column(Integer, ForeignKey('log.id'), primary_key=True)
    watthours = Column(Float) 
    use_time = Column(Float) 
    status = Column(Integer) 
    created = Column(DateTime) 
    credit = Column(Float,nullable=True) 
    status = Column(Integer) 

    def __init__(self,circuit,watthours,use_time,status,credit=0):
        Log.__init__(self,circuit)
        self.circuit = circuit
        self.watthours = watthours
        self.use_time = use_time 
        self.credit = credit
        self.created = get_now()
        self.status = status

    def get_property(self,string): 
        if string == "credit": 
            return self.credit
        elif string == "watt": 
            return self.watthours
        elif string == "power": 
            return self.use_time
        else: 
            raise NameError("Unable to find Property") 

class Job(Base):
    __tablename__ = "jobs" 
    id = Column(Integer, primary_key=True)
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    uuid  = Column(String) 
    start = Column(String) 
    end = Column(String)
    state = Column(Boolean)
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit, primaryjoin=circuit_id == Circuit.id)

    def __init__(self,circuit,state=True): 
        self.uuid = str(uuid.uuid4())
        self.start = get_now() 
        self.circuit = circuit
        self.state = state

    def url(self): 
        return "jobs/job/%s/" % self.id

    def toDict(self): 
        return {"uuid": self.uuid,
                "state" : self.state,
                "date": self.start,
                "type": self._type} 

    def toString(self): 
        return "job"


class JobMessage(Message): 
    """
    A class that repsents the text message for each message
    """ 
    __tablename__ = "job_message" 
    __mapper_args__ = {'polymorphic_identity': 'job_message'}
    id = Column(Integer,ForeignKey('message.id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    job = relation(Job, primaryjoin=job_id == Job.id)

    def __init__(self,job): 
        Message.__init__(self,job.circuit.meter.phone,str(uuid.uuid4())) 
        self.uuid = str(uuid.uuid4())
        self.job = job 

    @property
    def text(self): 
        return self.job.toString() 

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
                                                float(self.credit))

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
