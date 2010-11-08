#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8

import transaction
import random
import uuid 
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Unicode, DateTime,\
    ForeignKey, String, Float

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
    serial = Column(Integer) 
    slot = Column(Integer) 
    date = Column(DateTime) 
    

    def __init__(self,name,serial,slot):
        self.name = name
        self.serial = serial
        self.slot = slot 
        self.date = get_now() 
        self.uuid = str(uuid.uuid4())

    @property
    def url(self): 
        return "/meter/index/%s" % self.id

    def __str__(self): 
        return "<Meter %s>" % self.uuid

class Account(Base):
    """
    """
    __tablename__ = "account" 
    id = Column(Integer, primary_key=True)
    pin = Column(String) 
    uudi = Column(String) 
    name = Column(String)
    contact = Column(Integer) 
    secondary_contact = Column(Integer)         

    def __init__(self,name,contact,secondary_contact):
        self.name = name 
        self.contact = contact
        self.secondary_contact = secondary_contact
        self.uuid = str(uuid.uuid4())
        self.pin = self.get_pin() 

    def get_pin(self): 
        chars = "qwertyuipasdfghjkzxcvbnm"
        ints = "23456789" 
        return "%s%s" % ("".join(random.sample(chars,3)),
                      "".join(random.sample(ints,3)))
class Circuit(Base):
    """
    """
    __tablename__ = "circuit" 
    id = Column(Integer, primary_key=True)
    uudi = Column(String)
    meter = Column("meter",ForeignKey("meter.id"))
    account = Column("acccount",ForeignKey("account.id"))
    engery_max = Column(Float)
    power_max = Column(Float)
    status = Column(Integer) 

    def __init__(self,meter,account,engery_max,power_max):
        self.uuid = str(uuid.uuid4())
        self.meter = meter 
        self.account = account
        self.engery_max = engery_max
        self.power_max = power_max
        self.status = 1 

                       
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
