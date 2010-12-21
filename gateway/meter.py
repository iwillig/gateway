"""
Module for SS Gateway.
Handles all of the meter communcation 

"""
from gateway.models import Job, SystemLog, PrimaryLog, OutgoingMessage
from gateway.utils import make_message
from dateutil import parser

def valid(test, against):
    for key in against:
        if key not in test:
            return False
    return True

def make_delete(message, session): 
    job = session.query(Job).get(message["jobid"])
    if job:
        circuit = job.circuit
        job.state = False
        session.merge(job)        
        if job.type == "addcredit":
            session.add(OutgoingMessage(
                circuit.account.phone,
                make_message("credit.txt",
                             lang=circuit.account.lang,
                             account=circuit.pin,
                             status=circuit.get_rich_status()),
                incoming=message.uuid))            
        if message.get("cr"):
            circuit.credit = message["cr"]
            session.merge(circuit)
    else: 
        session.add(SystemLog(
                "Unable to find job message %s " % message))

def make_pp(message, circuit, session): 
    if valid(message.keys(),
             ['status', 'cid', 'tu', 'mid', 'wh', 'job']):
        date = parser.parse(message["ts"])
        log = PrimaryLog(
            date=date,
            circuit=circuit,
            watthours=message["wh"],
            use_time=message["tu"],
            credit=message.get("cr"),
            status=int(message["status"]))
        # override the credit and status value from the meter.
        circuit.credit = log.credit
        circuit.status = log.status
        session.add(log)
        session.merge(circuit)
    else:
        session.add(
            SystemLog(text="Unable to process message %s"
                      % message.uuid))


def make_nocw(message, circuit, session): 
    msg = OutgoingMessage(
            circuit.account.phone,
            make_message("nocw-alert.txt",
                         lang=circuit.account.lang,
                         account=circuit.pin))
    session.add(msg)
    session.flush()
    session.add(
        SystemLog(
            "Low credit alert for circuit %s sent to %s" % (circuit.pin,
                                                            msg.number)))

def make_lcw(message, circuit, session): 
    msg = OutgoingMessage(circuit.account.phone,
                          make_message("lcw-alert.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin))
    session.add(msg)
    # send email 

def make_md(message, circuit, session): 
    log = SystemLog(
        "Meter %s just falied, please investagte." % circuit.meter.name)
    session.add(log)
    # send email 

def make_ce(message, circuit, session): 
    log = SystemLog(
        "Circuit %s just failed, please investagate." % circuit.ip_address)
    session.add(log)
    # send email 
     
def make_pmax(message, circuit, session): 
    msg = OutgoingMessage(circuit.account.phone,
                          make_message("power-max-alert.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin))
    session.add(msg) 


def make_emax(message, circuit, session):
    msg = OutgoingMessage(circuit.account.phone,
                          make_message("energy-max-alert.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin))
    session.add(msg)


def make_sdc(message,circuit,session):
    pass 
