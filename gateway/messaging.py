import transaction
import threading
import datetime
import time
from Queue import Queue
from gateway.models import DBSession, Message,\
    Circuit

delimiter = "."
sendMessageQueue = Queue() 

def get_account(message): 
    session = DBSession() 
    (task,pin) = message["text"].split(delimiter) 
    try:         
        return session.query(Circuit).filter_by(pin=pin).first()
    except Exception,e: 
        print(e) 

def get_balance(message,language):     
    circuit = get_account(message)
    if language == "en": 
        response = "The remaining electricity \
credit on %s is %s as of %s" % (circuit.pin,
                                 circuit.credit,
                                 datetime.datetime.now().ctime())
    elif language =="fn": 
        response = "%s unites. Il restait %s unites sur\
la ligne %s le %s." % (circuit.credit,
                        circuit.credit,
                        circuit.pin,
                        datetime.datetime.now().ctime())
    Message.send_message(to=message["from"],text=response) 

def set_primary_contact(message,language): 
    pass 

def parse_message(): 
    while True: 
        message = sendMessageQueue.get()
        if message:
            text = message["text"].lower()  

            # allow users to check their balance
            if text.startswith("bal"):
                get_balance(message,"en")
            elif text.startswith("solde"): 
                get_balance(message,"fn")
                
            # allow consumers to set their primary contact 
            elif text.startswith("prim"): 
                set_primary_contact(message,"en")
            elif text.startswith(""): 
                set_primary_contact(message,"fn")             
            else: 
                print("unable to processs your message") 
        time.sleep(3) 

process_messages = threading.Thread(target=parse_message)
