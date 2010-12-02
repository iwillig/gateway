import os
from urlparse import parse_qs 
from mako.template import Template
from gateway.models import DBSession,\
    Circuit, Token, AddCredit, TurnOn,\
    TurnOff, PrimaryLog, OutgoingMessage, JobMessage, Meter, SystemLog

delimiter = "."
baseTemplate = "%s/gateway/templates/messages" % os.getcwd()

def make_message(template="error.txt",lang="fr",**kwargs): 
    """
    Function to look up message from templates.
    """
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

def clean_message(messageRaw): 
    """
    Does not basic cleaning of meter messages. 
    Step 1. Removes () 
    Step 2. Returns a new dict with only the first value
    """
    message = {} 
    messageBody = messageRaw.strip(")").strip("(")
    parsed_message = parse_qs(messageBody)    
    for k,v in parsed_message.iteritems(): 
        message[k] = v[0] 
    return message

def valid(test,against): 
    for key in against:
        if key not in test: 
            return False        
    return True 

def parse_meter_message(message,meter):
    """
    Parse message from the Meter
    Messages need to have () on each side 
    """
    session = DBSession()     
    messageBody = message.text.lower()     
    if messageBody.endswith(")") and messageBody.startswith("("): 
        messageDict = clean_message(messageBody)
        circuit = session.query(Circuit).\
            filter_by(ip_address=messageDict["cid"]).\
            filter_by(meter=meter).first() 
        if circuit: # double check that we have a circuit
            lang = circuit.account.lang # get the langauge 
            # ------------------------------
            #  Jobs messages. 
            # ------------------------------
            # primary log
            if messageDict['job'] == "pp":
                if valid(messageDict.keys(),
                         ['status', 'cid', 'tu', 'mid', 'wh', 'job']):
                    log = PrimaryLog(circuit=circuit,
                                     watthours=messageDict["wh"],
                                     use_time=messageDict["tu"],
                                     credit=messageDict.get("cr"),
                                     status=int(messageDict["status"]))
                    # override the credit and status value from the meter. 
                    circuit.credit = log.credit 
                    circuit.status = log.status
                    session.add(log)
                    session.merge(circuit)
                else: 
                    session.add(SystemLog(
                            text="Unable to process message %s" % message.uuid))
            # ------------------------------
            # Alerts. 
            # ------------------------------
            elif messageDict['job'] == "alerts": 
                # no credit warning
                if messageDict['alert'] == "nocw": 
                    session.add(OutgoingMessage(
                            circuit.account.phone,
                            make_message("nocw-alert.txt",
                                         lang=lang,
                                         account=circuit.pin),
                            incoming=message.uuid))
                # low credit warning
                elif messageDict['alert'] == "lcw": 
                    session.add(
                        OutgoingMessage(
                            circuit.account.phone,
                            make_message("lcw-alert.txt",
                                         lang=lang,
                                         account=circuit.pin),
                            incoming=message.uuid))
                # this alert is sent out if the meter is going down. 
                elif messageDict['alert'] == "md": 
                    pass 
                # component failure 
                elif messageDict['alert'] == "ce": 
                    pass 
                # circuit is off because power max crossed.
                elif messageDict['alert'] == "pmax":
                    session.add(
                        OutgoingMessage(
                            circuit.account.phone,
                            make_message("power-max-alert.txt",
                                         lang=lang,
                                         account=circuit.pin),
                            incoming=message.uuid))
                # circuit is off because enegry max crossed.
                elif messageDict['alerts'] == "emax": 
                    pass 
    else: 
        session.add(SystemLog(
                'Unable to parse message %s' % message.uuid))

def parse_message(message): 
    session = DBSession() 
    text = message.text.lower()  
    # ------------------------------
    # check to see if the messages is from a meter. 
    # if so, attepmt to parse the message.  
    # ------------------------------
    meter = session.query(Meter).filter_by(phone=str(message.number)).first()
    if meter:
        parse_meter_message(message,meter)
    # ------------------------------
    # Consumer messages
    # ------------------------------
    # allow consumers to check their balance.
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
        # fall through when we can not match a message
        pass

