import transaction
import datetime
import threading
import time
from Queue import Queue
from urlparse import parse_qs 
from gateway.models import DBSession, Message,\
    Circuit, Token, SystemLog, Account, AddCredit, TurnOn, TurnOff, PrimaryLog

delimiter = "."
sendMessageQueue = Queue() 

def get_circuit(message): 
    """ 
    Tries to match message to a circuit 
    """ 
    session = DBSession() 
    pin = message["text"].split(delimiter)[1]
    try:         
        return session.query(Circuit).filter_by(pin=pin).first()
    except Exception,e: 
        session.add(SystemLog("Unable to find circuit\
error@%s message@%s " % (e,message["uuid"])))
        return False

def get_token(message): 
    """
    Tries to match message to token.
    """
    session = DBSession() 
    token = message["text"].split(delimiter)[2] 
    try:
        return session.query(Token).\
            filter_by(state="new").filter_by(token=token).first() 
    except Exception,e: 
        session.add(SystemLog("Unable to find token\
error@%s message@%s" %(e,message["uuid"]))) 
        return False 

def get_balance(message,lang="en"):     
    """
    Allows users to check blance
    """
    session = DBSession() 
    circuit = get_circuit(message)
    if circuit:
        if lang == "en": 
            response = "The remaining electricity \
    credit on %s is %s as of %s" % (circuit.pin,
                                     circuit.credit,
                                     datetime.datetime.now().ctime())
        elif lang =="fr": 
            response = "%s unites. Il restait %s unites surla ligne %s le %s." % (circuit.credit,
                            circuit.credit,
                            circuit.pin,
                            datetime.datetime.now().ctime())
            session.add(Message.send_message(to=message["from"],text=response))
    else: 
        pass # failt to match any circuit 

def set_primary_contact(message,lang="en"): 
    """
    Allows users to set their primary contact number
    """
    session = DBSession() 
    circuit = get_circuit(message) 
    if circuit:
        account = session.\
            query(Account).get(circuit.account.id) 
        new_number = message["text"].split(delimiter)[2] 
        old_number = account.phone
        if lang == "en": 
            session.add(Message.send_message(
                message["from"],
                "The previous primary contact number %s\
 has been replaced with the number %s." % (old_number,
                                           new_number)))
            if new_number != message["from"]:
                session.add(Message.send_message(
                    new_number, 
                    "The previous primary contact number %s\
 has been replaced with the number %s." % (old_number,
                                           new_number)))
        elif lang == "fr": 
            session.add(Message.send_message(
                message["from"],
"Votre numero de contact est desormais %s. Le numero %s ne\
 sera plus utilise." % (new_number,
                        old_number)))
            if new_number != message["from"]:
                session.add(Message.send_message(
                    new_number, 
                    "Votre numero de contact est desormais %s. Le numero %s ne\
 sera plus utilise." % (new_number,
                        old_number)))
        account.phone = new_number
        session.merge(account) 
    else: 
        pass # fail to match any circuit 

def add_credit(message,lang="en"): 
    """
    Allows consumer to add credit to their account.
    Sends an outgoing message to the consumer. 
    """
    session = DBSession()
    circuit = get_circuit(message)
    token = get_token(message)
    if circuit and token:
        job = AddCredit(circuit=circuit,credit=token.value)
        session.add(Message.send_message(to=circuit.meter.phone,
                             text=job.toString()))
        session.add(job)
        if lang == "en": 
            session.add(Message.send_message(
                message["from"],"Credit has been\
 added to account %s. Status: %s" % (circuit.pin,circuit.status)))
        elif lang == "fr": 
            session.add(Message.send_message(message["from"],"Merci ! Le solde\
 de la ligne %s est desormais. La ligne est %s." % (circuit.pin,circuit.status)))
        token.state = "used"
    else: 
        pass 

def turn_circuit_on(message,lang="en"): 
    """
    Allows the consumer to turn their account on. 
    """
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:
        if circuit.account.lang == "en" : 
            session.add(Message.send_message(message["from"],"Account %s is %s.\
Remaining credit: %s" % (circuit.pin,circuit.status,circuit.credit)))
        elif circuit.account.lang == "fr" : 
            session.add(Message.\
                            send_message(message["from"],
                                         "%s La ligne %s est %s.Solde\
 restant: %s." % (circuit.status,circuit.pin,circuit.status,circuit.credit)))
        job = TurnOn(circuit)
        msg = Message.send_message(
            to=circuit.meter.phone,
            text=job.toString())
        session.add(msg) 
        session.add(job)
    else: 
        pass # 

def turn_circuit_off(message,lang="en"): 
    """
    Allows the consumer to turn off their account. 
    """
    session = DBSession() 
    circuit = get_circuit(message)
    if circuit:
        if circuit.account.lang == "en": 
            pass 
        elif circuit.account.lang == "fr": 
            pass 
        job = TurnOff(circuit) 
        msg = Message.send_message(
            to=circuit.meter.phone,
            text=job.toString())
        session.add(job)
        session.add(msg) 
    else: 
        pass # 

def set_primary_lang(message): 
    """
    Allows consumer to set their account lang 
    """ 

def use_history(message,lang="en"): 
    """
    Calculates use based on last 30 days of account activity  
    """
    if lang == "en": 
        pass 
    elif lang == "fr":
        pass 

def parse_meter_message(message):
    """
    Parse message from the Meter
    """
    session = DBSession() 
    parsed_message = parse_qs(message["text"].lower())
    job = parsed_message["job"][0] 
    circuit = session.query(Circuit).\
        filter_by(ip_address=parsed_message["cid"][0]).first()
    if job == "pp": # primary log 
        log = PrimaryLog(circuit=circuit,
                         watthours=parsed_message["wh"][0],
                         use_time=parsed_message["tu"][0],
                         credit=parsed_message["cr"][0],
                         status=int(parsed_message["status"][0]))
        session.add(log)
    elif job == "sp": # secondary log 
        pass 
    elif job == "alerts": 
        alert = parsed_message['alert'][0]
        if alert == "nocw": 
            if circuit.account.lang == "en": # send english alert
                alert = "Your electricity account %s has been turned off due to insuffcient funds, as of %s" % (circuit.pin,datetime.datetime.now().ctime())
                session.add(Message.send_message(to=circuit.account.phone,
                                                 text=alert))
            elif circuit.account.lang == "fr":  # send french 
                pass 
        if alert == "lcw": 
            if circuit.account.lang == "en": 
                alert = "Your electricity account {account} balance is low.Your remaining balance is less than 10, as of {time}." 
                session.add(Message.send_message(to=circuit.account.phone,
                                                 text=alert))
            elif circuit.account.lang == "fr": 
                pass 


def parse_message(message): 
    if message:
        text = message["text"].lower()  
        # allow consumers to check their balance        
        if text.startswith("job"): # collect all jobs
            parse_meter_message(message)
        elif text.startswith("bal"):
            get_balance(message)
        elif text.startswith("solde"): 
            get_balance(message,"fr")                
        # allow consumers to set their primary contact 
        elif text.startswith("prim"): 
            set_primary_contact(message)
        elif text.startswith("tel"): 
            set_primary_contact(message,"fr")             
        # allow consumers to add credit to their circuits
        elif text.startswith("add"): 
            add_credit(message) 
        elif text.startswith("recharge"): 
            add_credit(message,"fr") 
        # allow consumers to turn circuits on 
        elif text.startswith("on"): 
            turn_circuit_on(message)
        # allow consumers to turn circuit off
        elif text.startswith("off"): 
            turn_circuit_off(message)
        # allows consumers to get their use history
        elif text.startswith("use"): 
            use_history(message)
        elif text.startswith("conso"): 
            use_history(message,"fr")
        # allow users to set their primary contact language 
        elif text.startswith("english"): 
            set_primary_lang(message) 
        else: 
            # fall through if it does not
            Message.send_message(message["from"],
                                 "Unable to processs your message") 
    time.sleep(3) 

process_messages = threading.Thread(target=parse_message)
