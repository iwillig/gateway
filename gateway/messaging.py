import re 
from urlparse import parse_qs

from gateway.models import DBSession, Circuit
from gateway.models import Meter, SystemLog
from gateway import meter as meter_funcs


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

def findMeter(message):
    session = DBSession()
    meter = session.query(Meter).filter_by(phone=str(message.number)).first()
    if meter:
        return meter
    else:
        return False 
    
def parse_meter_message(message):
    """
    Parse message from the Meter
    Messages need to have () on each side
    use getattr 
    """
    session = DBSession()
    meter = findMeter(message)
    messageBody = message.text.lower()
    if re.match("^\(.*\)$",message.text.lower()):
        messageDict = clean_message(messageBody)
        if messageDict["job"] == "delete": 
            getattr(meter_funcs,"make_"+ messageDict["job"])(messageDict,session)
        else:
            circuit = session.query(Circuit).\
                filter_by(ip_address=messageDict["cid"]).\
                filter_by(meter=meter).first()
            if circuit:  # double check that we have a circuit
                if messageDict['job'] == "pp":
                    getattr(meter_funcs,
                            "make_"+ messageDict["job"])(messageDict,
                                                         circuit,session)
                elif messageDict['job'] == "alert":
                    getattr(meter_funcs,
                            "make_"+ messageDict["alert"])(messageDict,
                                                           circuit,
                                                           session)
    else:
        session.add(SystemLog(
                'Unable to parse message %s' % message.uuid))

