#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8

import transaction
import random
import uuid 
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Unicode, DateTime,\
    ForeignKey, String, Float, Boolean

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session (sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

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
        return [x for x in 
                session.query(Circuit).filter_by(meter=self.id)] 

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
    contact = Column(Integer) 
    secondary_contact = Column(Integer)         

    def __init__(self,name,contact,secondary_contact):
        self.name = name 
        self.contact = contact
        self.secondary_contact = secondary_contact


class Circuit(Base):
    """
    """
    __tablename__ = "circuit" 
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    date = Column(DateTime) 
    pin = Column(String) 
    meter = Column("meter",ForeignKey("meter.id"))
    energy_max = Column(Float)
    power_max = Column(Float)
    status = Column(Integer) 
    ip_address = Column(String) 

    def __init__(self,meter,energy_max,power_max,ip_address):
        self.date = get_now()
        self.uuid = str(uuid.uuid4())
        self.pin = self.get_pin() 
        self.meter = meter 
        self.energy_max = energy_max
        self.power_max = power_max
        self.ip_address = ip_address
        self.status = 1 

    def get_pin(self): 
        chars = "qwertyuipasdfghjkzxcvbnm"
        ints = "23456789" 
        return "%s%s" % ("".join(random.sample(chars,3)),
                      "".join(random.sample(ints,3)))

    def get_meter(self): 
        session = DBSession()
        return session.query(Meter).get(self.meter)

    def toggle_status(self): 
        session = DBSession() 
        if self.status == 0: 
            session.add(TurnOn(circuit=self))
        else:             
            session.add(TurnOff(circuit=self))

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
    to = Column(Integer) 
    origin = Column(Integer) 
    
    
    def __init__(self,uuid,incoming,sent,text,origin,to=18182124554):
        self.date = get_now() 
        self.uuid = uuid
        self.incoming = incoming
        self.sent = sent 
        self.text = text 
        self.to = to 
        self.origin = origin 

    def toJSON(self): 
        return { "from" : self.origin,
                 "to"   : self.to,
                 "uuid" : self.uuid,
                 "text" : self.text,
                 "id"   : self.id, } 
        
    def __unicode__(self): 
        return "Messsage <%s>" % self.uuid

class Logs(Base): 
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    uuid = Column(String) 
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    
    def __init__(self): 
        self.date = get_now() 
        self.uuid = str(uuid.uuid4)

class PrimaryLog(Logs): 
    __tablename__ = "primary_log" 
    __mapper_args__ = {'polymorphic_identity': 'primary_log'}
    id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    circuit  = Column("circuit",ForeignKey("circuit.id"))
    watthours = Column(Integer) 
    use_time = Column(Integer) 
    status = Column(Integer) 
    time = Column(Integer) 

    def __init__(self,circuit,watthours,use_time,status,time):
        Logs.__init__(self,)
        self.circuit = circuit
        self.watthours = watthours
        self.use_time = use_time 
        self.time = time
    

class Job(Base):
    __tablename__ = "jobs" 
    id = Column(Integer, primary_key=True)
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    #circuit  = Column("circuit",ForeignKey("circuit.id"))
        

class AddCredit(Job):
    __tablename__ = "addcredit" 
    __mapper_args__ = {'polymorphic_identity': 'addcredit'}
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    credit = Column(Integer) 
        
    def toString(self): 
        return ""

class TurnOff(Job):
    __tablename__ = "turnoff" 
    __mapper_args__ = {'polymorphic_identity': 'turnoff'}
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    

    def toString(self): 
        return ""
        
class TurnOn(Job):
    __tablename__ = "turnon"
    __mapper_args__ = {'polymorphic_identity': 'turnon'}
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

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
