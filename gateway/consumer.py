"""
Functions to response to consumer messages
"""
from gateway.models import DBSession
from gateway.models import Circuit
from gateway.models import Token
from gateway.models import AddCredit
from gateway.models import TurnOn
from gateway.models import TurnOff
from gateway.models import OutgoingMessage
from gateway.models import JobMessage
from gateway.models import Meter
from gateway.models import SystemLog
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
            session.add(job)
            session.flush()
            session.add(JobMessage(job, circuit.account.phone,
                                   incoming=message.uuid))
            token.state = "used"
            session.merge(token)
            session.merge(circuit)


def turn_circuit_on(message):
    """Allows the consumer to turn their account on."""

    circuit = get_circuit(message)
    if circuit:
        circuit.turnOn(incoming=message.uuid)


def turn_circuit_off(message, lang="fr"):
    """ Creates a new job called turn_off """
    circuit = get_circuit(message)
    if circuit:
        circuit.turnOff(incoming=message.uuid)


def set_primary_lang(message):
    """ Allows consumer to set their account lang
    """


def use_history(message, lang="en"):
    """
    Calculates use based on last 30 days of account activity
    """
