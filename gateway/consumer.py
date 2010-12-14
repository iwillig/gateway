from gateway.models import DBSession, \
    Circuit, Token, AddCredit, TurnOn, \
    TurnOff, OutgoingMessage, \
    JobMessage, Meter, SystemLog
from gateway.utils import make_message

delimiter = "."

def get_circuit(message):
    """Queris the database to find circuit
    Returns the circuit or false 
    """
    session = DBSession()
    pin = message.text.split(delimiter)[1].lower()
    circuit = session.query(Circuit).filter_by(pin=pin).first()
    if circuit:
        return circuit
    else:
        msg = OutgoingMessage(
            message.number,
            make_message("no-circuit.txt", lang=message.langauge),
            incoming=message.uuid)
        session.add(msg)
        return False


def get_token(message):
    """Tries to match message to token."""
    session = DBSession()
    tokenNumber = message.text.split(delimiter)[2]
    token = session.query(Token).\
            filter_by(state="new").filter_by(token=tokenNumber).first()
    if token:
        return token
    else:
        msg = OutgoingMessage(
                message.number,
                make_message("no-token.txt", lang=message.langauge),
                incoming=message.uuid)
        session.add(msg)
        return False


def get_balance(message):
    """Allows users to check blance"""
    session = DBSession()
    circuit = get_circuit(message)
    langauge = message.langauge
    if circuit:        
        msg = OutgoingMessage(
            message.number,
            make_message("bal.txt",
                         lang=langauge,
                         account=circuit.pin,
                         credit=circuit.credit),
            incoming=message.uuid)
        session.add(msg)



def set_primary_contact(message):
    """Allows users to set their primary contact number"""
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:        
        new_number = message.text.split(delimiter)[2]
        old_number = circuit.account.phone
        messageBody = make_message("tel.txt", lang=message.langauge,
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
    token = get_token(message)
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


def turn_circuit_on(message):
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


