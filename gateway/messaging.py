import transaction
import threading
import datetime
import time
from Queue import Queue
from gateway.models import DBSession, Message,\
    Circuit, Token, SystemLog

delimiter = "."
sendMessageQueue = Queue() 

def get_circuit(message): 
    """ 
    Tries to match message to a circuit 
    """ 
    session = DBSession() 
    (task,pin) = message["text"].split(delimiter) 
    try:         
        return session.query(Circuit).filter_by(pin=pin).first()
    except Exception,e: 
        session.add(SystemLog("Unable to find circuit\
error@%s message@%s " % (e,message["uuid"])))
        transaction.commit() 
        return False

def get_token(message): 
    """
    Tries to match message to token.
    """
    session = DBSession() 
    (task,pin,token) = message["text"].split(delimiter) 
    try:
        return session.query(Token).filter_by(token=token).first() 
    except Exception,e: 
        session.add(SystemLog("Unable to find token\
error@%s message@%s" %(e,message["uuid"] ))) 
        return False 

def get_balance(message,lang="en"):     
    """
    Allows users to check blance
    """
    circuit = get_circuit(message)
    if circuit:
        if lang == "en": 
            response = "The remaining electricity \
    credit on %s is %s as of %s" % (circuit.pin,
                                     circuit.credit,
                                     datetime.datetime.now().ctime())
        elif lang =="fr": 
            response = "%s unites. Il restait %s unites sur\
    la ligne %s le %s." % (circuit.credit,
                            circuit.credit,
                            circuit.pin,
                            datetime.datetime.now().ctime())
        Message.send_message(to=message["from"],text=response) 
    else: 
        pass # failt to match any circuit 

def set_primary_contact(message,lang="en"): 
    session = DBSession() 
    circuit = get_circuit(message) 
    if circuit:
        account = circuit.account
        import ipdb; ipdb.set_trace() 
        account.phone = message.split(delimiter)[2] 
        if lang == "en": 
            pass 
        elif lang == "fr": 
            pass 
    else: 
        pass # fail to match any circuit 

def add_credit(message,lang="en"): 
    circuit = get_circuit(message)
    token = get_token(message)
    if circuit and token:
        if lang == "en": 
            pass 
        elif lang == "fr": 
            pass 

def turn_circuit_on(message,lang="en"): 
    circuit = get_circuit(message)
    if circuit:
        if lang == "en": 
            pass 

def turn_circuit_off(message,lang="en"): 
    # get lang from account
    pass 

def use_history(message,lang="en"): 
    if lang == "en": 
        pass 
    elif lang == "fr":
        pass 

def parse_message(): 
    while True: 
        message = sendMessageQueue.get()
        # check to see if message matchs any known task
        if message:
            text = message["text"].lower()  
            # allow consumers to check their balance
            if text.startswith("bal"):
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
            else: 
                # fall through if it does not
                Message.send_message(message["from"],
                                     "Unable to processs your message") 
        time.sleep(3) 

process_messages = threading.Thread(target=parse_message)
