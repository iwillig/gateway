import os
from urlparse import parse_qs 
from mako.template import Template
from gateway.models import DBSession,\
    Circuit, Token, AddCredit, TurnOn,\
    TurnOff, PrimaryLog, OutgoingMessage, JobMessage, Meter 

delimiter = "."
baseTemplate = "%s/gateway/templates/messages" % os.getcwd()

def make_message(template="error.txt",lang="fr",**kwargs): 
    templateName = "%s/%s/%s" % (baseTemplate,lang,template) 
    template = Template(filename=templateName).render(**kwargs)
    return template
    
def get_circuit(message,lang="fr"): 
    """ 
    Tries to match message to a circuit 
    """ 
    session = DBSession() 
    pin = message.text.split(delimiter)[1]
    circuit =  session.query(Circuit).filter_by(pin=pin).first()
    if circuit: 
        return circuit
    else:
        session.add(OutgoingMessage(
                message.number,
                make_message("no-circuit.txt",lang=lang),
                incoming=message.uuid))
        return False

def get_token(message,lang): 
    """
    Tries to match message to token.
    """
    session = DBSession() 
    tokenNumber = message.text.split(delimiter)[2] 
    token = session.query(Token).\
            filter_by(state="new").filter_by(token=tokenNumber).first()
    if token:
        return token 
    else:         
        session.add(OutgoingMessage(
                message.number,
                make_message("no-token.txt",lang=lang),
                incoming=message.uuid))
        return False

def get_balance(message,lang="en"):     
    """
    Allows users to check blance
    """
    session = DBSession() 
    circuit = get_circuit(message,lang=lang)
    if circuit:
        session.add(OutgoingMessage(
                message.number,
                make_message("bal.txt",
                             lang=lang,
                             account=circuit.pin,
                             credit=circuit.credit),
                incoming=message.uuid))

def set_primary_contact(message,lang="en"): 
    """
    Allows users to set their primary contact number
    """
    session = DBSession() 
    circuit = get_circuit(message,lang=lang) 
    if circuit:
        new_number = message.text.split(delimiter)[2] 
        old_number = circuit.account.phone
        messageBody = make_message("tel.txt",lang=lang,
                                   old_number=old_number,
                                   new_number=new_number)
        session.add(OutgoingMessage(message.number,
                                    messageBody,
                                    incoming=message.uuid))
        if new_number != message.number:
            session.add(OutgoingMessage(
                    new_number, 
                    messageBody,incoming=message.uuid))
        account = circuit.account
        account.phone = new_number
        session.merge(account) 

        
def add_credit(message,lang="en"): 
    """
    Allows consumer to add credit to their account.
    Sends an outgoing message to the consumer. 
    """
    session = DBSession()
    circuit = get_circuit(message)
    token = get_token(message,lang=lang)
    if circuit:
        if token:
            job = AddCredit(circuit=circuit,credit=token.value)
            session.add(JobMessage(job))
            session.add(OutgoingMessage(
                    message.number,
                    make_message("credit.txt",
                                 lang=lang,
                                 account=circuit.pin,
                                 status=circuit.get_rich_status()),
                    incoming=message.uuid))
                # update token database 
            token.state = "used"
            session.merge(token) 
            session.merge(circuit)

def turn_circuit_on(message,lang="en"): 
    """
    Allows the consumer to turn their account on. 
    """
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:
        lang = circuit.account.lang 
        # check to make sure that the circuit has credit 
        if circuit.credit > 0:
            messageBody = make_message("toggle.txt",lang=lang,
                                       account=circuit.pin,
                                       status=circuit.get_rich_status(),
                                       credit=circuit.credit)
            job = TurnOn(circuit)
            session.add(JobMessage(job))
            session.add(job)
        else: 
            messageBody = make_message("toggle-error.txt",
                                       lang=lang,
                                       account=circuit.pin)                
        # send the result back to the consumer
        session.add(OutgoingMessage(message.number,
                                    messageBody,
                                    incoming=message.uuid)) 


    
def turn_circuit_off(message,lang="en"): 
    """
    Allows the consumer to turn off their account. 
    """
    session = DBSession() 
    circuit = get_circuit(message)
    if circuit:        
        lang = circuit.account.lang 
        job = TurnOff(circuit) 
        session.add(OutgoingMessage(
                message.number,
                make_message("toggle.txt",
                             lang=lang,
                             account=circuit.pin,
                             status=circuit.get_rich_status(),
                             credit=circuit.credit),
                incoming=message.uuid))
        session.add(JobMessage(job))
        session.add(job)


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

def parse_meter_message(message,meter):
    """
    Parse message from the Meter
    """
    session = DBSession()     
    parsed_message = parse_qs(message.text.lower())
    job = parsed_message["job"][0] 
    circuit = session.query(Circuit).\
        filter_by(ip_address=parsed_message["cid"][0]).\
        filter_by(meter=meter).first() 
    lang = circuit.account.lang 
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
                session.add(OutgoingMessage(
                        circuit.account.phone,
                        make_message("nocw-alert.txt",
                                     lang=lang,
                                     account=circuit.pin),
                        incoming=message.uuid))
            if alert == "lcw": 
                session.add(
                    OutgoingMessage(
                        circuit.account.phone,
                        make_message("lcw-alert.txt",
                                     lang=lang,
                                     account=circuit.pin),
                        incoming=message.uuid))

def parse_message(message): 
    session = DBSession() 
    text = message.text.lower()  
    import ipdb; ipdb.set_trace()
    meter = session.query(Meter).filter_by(phone=str(message.number)).first()
    if meter:
        parse_meter_message(message,meter)
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
        pass

