import os
import re 
from urlparse import parse_qs
from mako.template import Template
from gateway.models import DBSession, \
    Circuit, Token, AddCredit, TurnOn, \
    TurnOff, PrimaryLog, OutgoingMessage, \
    JobMessage, Meter, SystemLog, Job

delimiter = "."
baseTemplate = "%s/gateway/templates/messages" % os.getcwd()


def make_message(template="error.txt", lang="fr", **kwargs):
    """Builds a template based on name and langauge with kwargs passed to the template.. 
    Returns a template object 
    """
    templateName = "%s/%s/%s" % (baseTemplate, lang, template)
    template = Template(filename=templateName).render(**kwargs)
    return template


def get_circuit(message, lang="fr"):
    """Queries the database to find circuit
    Returns the circuit or false 
    """
    session = DBSession()
    pin = message.text.split(delimiter)[1]
    circuit = session.query(Circuit).filter_by(pin=pin).first()
    if circuit:
        return circuit
    else:
        session.add(OutgoingMessage(
                message.number,
                make_message("no-circuit.txt", lang=lang),
                incoming=message.uuid))
        return False


def get_token(message, lang):
    """Tries to match message to token."""
    session = DBSession()
    tokenNumber = message.text.split(delimiter)[2]
    token = session.query(Token).\
            filter_by(state="new").filter_by(token=tokenNumber).first()
    if token:
        return token
    else:
        session.add(OutgoingMessage(
                message.number,
                make_message("no-token.txt", lang=lang),
                incoming=message.uuid))
        return False


def get_balance(message, lang="en"):
    """Allows users to check blance"""
    session = DBSession()
    circuit = get_circuit(message, lang=lang)
    if circuit:
        session.add(OutgoingMessage(
                message.number,
                make_message("bal.txt",
                             lang=lang,
                             account=circuit.pin,
                             credit=circuit.credit),
                incoming=message.uuid))


def set_primary_contact(message, lang="en"):
    """Allows users to set their primary contact number"""
    session = DBSession()
    circuit = get_circuit(message, lang=lang)
    if circuit:
        new_number = message.text.split(delimiter)[2]
        old_number = circuit.account.phone
        messageBody = make_message("tel.txt", lang=lang,
                                   old_number=old_number,
                                   new_number=new_number)
        session.add(OutgoingMessage(message.number,
                                    messageBody,
                                    incoming=message.uuid))
        if new_number != message.number:
            session.add(OutgoingMessage(
                    new_number,
                    messageBody,
                    incoming=message.uuid))
        account = circuit.account
        account.phone = new_number
        session.merge(account)


def add_credit(message, lang="en"):
    """Allows consumer to add credit to their account.
    Sends an outgoing message to the consumer.
    """
    session = DBSession()
    circuit = get_circuit(message)
    token = get_token(message, lang="en")
    if circuit:
        if token:
            job = AddCredit(circuit=circuit, credit=token.value)
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


def turn_circuit_on(message, lang="en"):
    """Allows the consumer to turn their account on."""
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:
        lang = circuit.account.lang 
        # check to make sure that the circuit has credit
        if circuit.credit > 0:
            messageBody = make_message("toggle.txt",
                                       lang=lang,
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


def turn_circuit_off(message, lang="en"):
    """ Creates a new job called turn_off """
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
    """ Allows consumer to set their account lang
    """


def use_history(message, lang="en"):
    """
    Calculates use based on last 30 days of account activity
    """

def clean_message(messageRaw):
    """  Does the basic cleaning of meter messages.
    Step 1. Removes ()
    Step 2. Returns a new dict with only the first value 
    of each key value pair
    """
    message = {}
    messageBody = messageRaw.strip(")").strip("(")
    parsed_message = parse_qs(messageBody)
    for k, v in parsed_message.iteritems():
        message[k] = v[0]
    return message


def valid(test, against):
    for key in against:
        if key not in test:
            return False
    return True

def mark_job_inactive(message, session): 
    job = session.query(Job).get(message["jobid"])
    if job:
        circuit = job.circuit
        job.state = False
        session.merge(job)
        if message["cr"]:
            circuit.credit = message["cr"]
            session.merge(circuit)
    else: 
        session.add(SystemLog(
                "Unable to find job message %s " % message))

def make_log(message, circuit, session): 
    if valid(message.keys(),
             ['status', 'cid', 'tu', 'mid', 'wh', 'job']):
        log = PrimaryLog(circuit=circuit,
                         watthours=message["wh"],
                         use_time=message["tu"],
                         credit=message.gte("cr"),
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


def make_no_credit_alert(message, circuit, session): 
    session.add(OutgoingMessage(
            circuit.account.phone,
            make_message("nocw-alert.txt",
                         lang=circuit.lang,
                         account=circuit.pin),
            incoming=message.uuid))    
    session.add(
        SystemLog(
            "Low credit alert for circuit %s sent to %s" % (circuit,
                                                            message.number)))

def make_low_credit_alert(message, circuit, session): 
    msg = OutgoingMessage(circuit.account.phone,
                          make_message("lcw-alert.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin),
                          incoming=message.uuid)
    session.add(msg)
    # send email 

def make_meter_down_alert(message, circuit, session): 
    log = SystemLog(
        "Meter %s just falied, please investagte." % circuit.meter)
    session.add(log)
    # send email 

def make_component_alert(message, circuit, session): 
    log = SystemLog(
        "Component %s just failed, please investagate." % circuit)
    session.add(log) 
    # send email 
     
def make_power_max_alert(message, circuit, session): 
    msg = OutgoingMessage(circuit.account.phone,
                          make_message("power-max-alert.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin),
                          incoming=message.uuid)
    session.add(msg) 
    
def parse_meter_message(message, meter):
    """
    Parse message from the Meter
    Messages need to have () on each side
    use getattr 
    """
    session = DBSession()
    messageBody = message.text.lower()
    if messageBody.endswith(")") and messageBody.startswith("("):
        messageDict = clean_message(messageBody)
        if messageDict["job"] == "delete": 
            mark_job_inactive(messageDict,session)
        else:
            circuit = session.query(Circuit).\
                filter_by(ip_address=messageDict["cid"]).\
                filter_by(meter=meter).first()
            if circuit:  # double check that we have a circuit
                if messageDict['job'] == "pp":
                    make_log(messageDict,circuit,session)
                elif messageDict['job'] == "alerts":
                    # no credit warning
                    if messageDict['alert'] == "nocw":
                        make_no_credit_alert(messageDict,circuit,session)
                    elif messageDict['alert'] == "lcw":
                        make_low_credit_alert(messageDict,circuit,session)
                    elif messageDict['alert'] == "md":
                        make_meter_down_alert(messageDict, circuit,session)
                    # component failure
                    elif messageDict['alert'] == "ce":
                        make_component_alert(messageDict,circuit,session)
                    # circuit is off because power max crossed.
                    elif messageDict['alert'] == "pmax":
                    # circuit is off because enegry max crossed.
                        make_power_max_alert(messageDict, circuit, session)
                    elif messageDict['alerts'] == "emax":
                        pass
    else:
        session.add(SystemLog(
                'Unable to parse message %s' % message.uuid))

# dictionary that allows use to match incoming messages 
# from the consumer. 
consumer_matchers = [ 
    { "matcher" : "^bal",
      "lang"    : "en",
      "func"    : get_balance },
    { "matcher" : "^solde",
      "lang"    : "fr",
      "func"    : get_balance},          
    { "matcher" : "^prim",
      "lang"    : "en",
      "func"    : set_primary_contact },
    { "matcher" : "^tel",
      "lang"    : "fr",
      "func"    : set_primary_contact },
    { "matcher" : "^add",
      "lang"    : "en",
      "func"    : add_credit },
    { "matcher" : "^recharge",
      "lang"    : "fr",
      "func"    : add_credit },
    { "matcher" : "^on",
      "lang"    : "fr",
      "func"    : turn_circuit_on},
    { "matcher" : "^off",
      "lang"    : "fr",
      "func"    : turn_circuit_off } 
    ] 

def match_consumer_message(message):
    session = DBSession() 
    for match in consumer_matchers: 
        if re.match(match["matcher"], message.text.lower()): 
            match["func"](message, match["lang"])                
        else: 
            session.add(
                SystemLog("Unable to parse consumer message %s" % message))

def parse_message(message):
    session = DBSession()
    # ------------------------------
    # check to see if the messages is from a meter.
    # if so, attepmt to parse the message.
    # ------------------------------
    meter = session.query(Meter).filter_by(phone=str(message.number)).first()
    if meter:
        parse_meter_message(message, meter)
    # match consumer messages
    else: 
        match_consumer_message(message)        
