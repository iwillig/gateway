import re
from urlparse import parse_qs

from gateway.models import DBSession, Circuit
from gateway.models import Meter, SystemLog
from gateway import meter as meter_funcs

session = DBSession()


def clean_message(messageRaw):
    """  Does the basic cleaning of meter messages.
    Step 1. Removes ()
    Step 2. Returns a new dict with only the first value
    of each key value pair
    """
    messageBody = messageRaw.text.lower()
    messageBody = messageBody.strip(")").strip("(")
    message = {}
    parsed_message = parse_qs(messageBody)
    for k, v in parsed_message.iteritems():
        message[k] = v[0]
    message['meta'] = messageRaw
    return message


def findMeter(message):
    """
    Takes a message object and returns either a meter or none.
    Looks up the meter based on the message's number.
    """
    meter = session.query(Meter).filter_by(phone=str(message.number)).first()
    if meter:
        return meter
    else:
        return False


def findCircuit(message, meter):
    circuit = session.query(Circuit).\
              filter_by(ip_address=message["cid"]).\
              filter_by(meter=meter).first()
    if circuit:
        return circuit


def parse_meter_message(message):
    """ Parse message from the Meter. Takes a message object and returns
    nothing. Logs an exception if the message is unable to be parsed.
    """
    meter = findMeter(message)
    messageBody = message.text.lower()
    if re.match("^\(.*\)$", message.text.lower()):
        messageDict = clean_message(message)
        if messageDict["job"] == "delete":
            getattr(meter_funcs,
                    "make_" + messageDict["job"])(messageDict, session)
        else:
            circuit = findCircuit(messageDict, meter)
            if circuit:  # double check that we have a circuit
                if messageDict['job'] == "pp":
                    getattr(meter_funcs,
                            "make_" + messageDict["job"])(messageDict,
                                                         circuit,
                                                         session)
                elif messageDict['job'] == "alerts":
                    getattr(meter_funcs,
                            "make_" + messageDict["alert"])(messageDict,
                                                           circuit,
                                                           session)
    else:
        session.add(SystemLog(
                'Unable to parse message %s' % message.uuid))
