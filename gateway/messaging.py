import datetime
from urlparse import parse_qs 
from mako.template import Template

from gateway.models import DBSession,\
    Circuit, Token, SystemLog, Account, AddCredit, TurnOn,\
    TurnOff, PrimaryLog, OutgoingMessage, JobMessage, Meter 

delimiter = "."
baseTemplate = "gateway/templates/messages/"

def make_response(template="error.txt",**kwargs): 
    templateName = baseTemplate + str(template) 
    template = Template(filename=templateName).render(**kwargs)
    return template
    
def get_circuit(message): 
    """ 
    Tries to match message to a circuit 
    """ 
    session = DBSession() 
    pin = message.text.split(delimiter)[1]
    try:         
        return session.query(Circuit).filter_by(pin=pin).first()
    except Exception,e: 
        session.add(SystemLog("Unable to find circuit\
error@%s message@%s " % (e,message.uuid)))
        return False

def get_token(message): 
    """
    Tries to match message to token.
    """
    session = DBSession() 
    token = message.text.split(delimiter)[2] 
    try:
        return session.query(Token).\
            filter_by(state="new").filter_by(token=token).first() 
    except Exception,e: 
        session.add(SystemLog("Unable to find token\
error@%s message@%s" %(e,message.uuid))) 
        return False 

def get_balance(message,lang="en"):     
    """
    Allows users to check blance
    """
    response = ""
    session = DBSession() 
    circuit = get_circuit(message)
    if lang == "en": 
        if circuit:
            response = make_response("bal/en.txt",
                                     account=circuit.pin,
                                     credit=circuit.credit)                       
        else: 
            response = make_response("errors/no-circuit-en.txt")
    elif lang =="fr": 
        if circuit:
            response = make_response("bal/fr.txt",
                                     account=circuit.pin,
                                     credit=circuit.credit)
        else: 
            response = make_response("errors/no-circuit-fr.txt")
    session.add(OutgoingMessage(message.number,
                                    response,incoming=message.uuid))


def set_primary_contact(message,lang="en"): 
    """
    Allows users to set their primary contact number
    """
    session = DBSession() 
    circuit = get_circuit(message) 
    if circuit:
        account = session.\
            query(Account).get(circuit.account.id) 
        new_number = message.text.split(delimiter)[2] 
        old_number = account.phone
        if lang == "en": 
            session.add(OutgoingMessage(message.number,
                "The previous primary contact number %s\
 has been replaced with the number %s." % (old_number,
                                           new_number),incoming=message.uuid))
            if new_number != message.number:
                session.add(OutgoingMessage(
                    new_number, 
                    "The previous primary contact number %s\
 has been replaced with the number %s." % (old_number,
                                           new_number),incoming=message.uuid))
        elif lang == "fr": 
            session.add(OutgoingMessage(
                message.number,
"Votre numero de contact est desormais %s. Le numero %s ne\
 sera plus utilise." % (new_number,
                        old_number),incoming=message.uuid))
            if new_number != message.number:
                session.add(OutgoingMessage(
                    new_number, 
                    "Votre numero de contact est desormais %s. Le numero %s ne\
 sera plus utilise." % (new_number,
                        old_number),incoming=message.uuid))
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
    if circuit:
        if token:
            # method circuit.add_credit() that takes care of everything.
            job = AddCredit(circuit=circuit,credit=token.value)
            session.add(JobMessage(job))
            if lang == "en": # figure out correct response for english 
                response = make_response("credit/en.txt",account=circuit.pin,status=circuit.status)
            elif lang == "fr": 
                response = make_response("credit/fr.txt",account=circuit.pin,status=circuit.status)
            session.add(
                OutgoingMessage(
                    message.number,response,incoming=message.uuid))
            # update token database 
            token.state = "used"
            session.merge(token) 
            session.merge(circuit)
        else: 
            session.add(
                OutgoingMessage(
                    message.number,"Thats a used token!!, you can't use it again",
                    incoming=message.uuid))
    else: 
        session.add(
            OutgoingMessage(
                message.number,"Unable to find circuit",
                incoming=message.uuid))


def turn_circuit_on(message,lang="en"): 
    """
    Allows the consumer to turn their account on. 
    """
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:
        # check to make sure that the circuit has credit 
        if circuit.credit > 0:
            if circuit.account.lang == "en" : 
                response = "Account %s is %s.Remaining credit: %s" % (circuit.pin,
                                                                      circuit.status,
                                                                      circuit.credit)
            elif circuit.account.lang == "fr" : 
                response = "La ligne %s est %s.Solde restant: %s." % (circuit.pin,
                                                                         circuit.status,
                                                                         circuit.credit)
            job = TurnOn(circuit)
            session.add(JobMessage(job))
            session.add(job)
        else: 
            if circuit.account.lang == "en": 
                response = "Your request to activate account %s failed.\
Remaining credit is zero. Please add more credit to your account." % circuit.pin
            elif circuit.account.lang == "fr":
                response = "ECHEC. Vous ne pouvez pas activer la ligne\
 %s car le solde est zero. Ajoutez des unites d'abord." % circuit.pin
        # send the result back to the consumer
        session.add(OutgoingMessage(message.number,response,incoming=message.uuid)) 
    else: 
        session.add(
            OutgoingMessage(
                message.number,
                "Unable to process your account",
                incoming=message.uuid))

    
def turn_circuit_off(message,lang="en"): 
    """
    Allows the consumer to turn off their account. 
    """
    session = DBSession() 
    circuit = get_circuit(message)
    if circuit:
        if circuit.account.lang == "en": 
            response = "Account %s is %s. Remaining credit: %s" % (circuit.pin,
                                                                   circuit.status,
                                                                   circuit.credit)
        elif circuit.account.lang == "fr": 
            response = "La ligne %s est %s. Solde restant: %s" % (circuit.pin,
                                                                  circuit.status,
                                                                  circuit.credit)
        job = TurnOff(circuit) 
        session.add(OutgoingMessage(message.number,response,incoming=message.uuid))
        session.add(JobMessage(job))
        session.add(job)
    else: 
        session.add(
            OutgoingMessage(
                message.number,
                "Unable to find your circuit",
                incoming=message.uuid))


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
    parsed_message = parse_qs(message.text.lower())
    job = parsed_message["job"][0] 
    meter = session.query(Meter).filter_by(phone=message.number).first()
    circuit = session.query(Circuit).\
        filter_by(ip_address=parsed_message["cid"][0]).\
        filter_by(meter=meter).first() 
    if circuit:
        if job == "pp": # primary log 
            log = PrimaryLog(circuit=circuit,
                             watthours=parsed_message["wh"][0],
                             use_time=parsed_message["tu"][0],
                             credit=parsed_message["cr"][0],
                             status=int(parsed_message["status"][0]))
            circuit.credit = log.credit
            session.add(log)
            session.merge(circuit)
        elif job == "alerts": 
            alert = parsed_message['alert'][0]
            if alert == "nocw": 
                if circuit.account.lang == "en": # send english alert
                    alert = "Your electricity account %s has \
been turned off due to insuffcient funds, as of %s" % (circuit.pin,datetime.datetime.now().ctime())
                    session.add(OutgoingMessage(circuit.account.phone,
                                                text=alert,
                                                incoming=message.uuid))
                elif circuit.account.lang == "fr":  # send french 
                    pass 
            if alert == "lcw": 
                if circuit.account.lang == "en": 
                    alert = "Your electricity account {account} balance is low.Your remaining balance is less than 10, as of {time}." 
                    session.add(OutgoingMessage(circuit.account.phone,
                                                text=alert,
                                                incoming=message.uuid))
                elif circuit.account.lang == "fr": 
                    pass 


def parse_message(message): 
    session = DBSession() 
    meterNumbers = [x.phone for x in session.query(Meter).all()] 
    text = message.text.lower()  
    if message.number in meterNumbers:
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
        # fall through we can not match a message
        session.add(OutgoingMessage(
                message.number,
                "Unable to processs your message",incoming=message.uuid))

