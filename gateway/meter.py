"""
Module for SS Gateway.
Handles all of the meter communcation
"""
from dateutil import parser
from gateway.models import Job
from gateway.models import SystemLog
from gateway.models import PrimaryLog
from gateway.models import IncomingMessage
from gateway.utils import make_message_body


def valid(test, against):
    for key in against:
        if key not in test:
            return False
    return True


def make_delete(msgDict, session):
    """
    Responses to a delete messsage from the meter.
    """
    session.add(SystemLog("%s" % msgDict))
    job = session.query(Job).get(msgDict["jobid"])
    if job:
        if len(job.job_message) is not 0:
            incoming_uuid = job.job_message[0]
        elif len(job.kannel_job_message) is not 0:
            incoming_uuid = job.kannel_job_message[0].incoming
        originMsg = session.query(IncomingMessage).\
                    filter_by(uuid=incoming_uuid).first()
        circuit = job.circuit
        interface = circuit.meter.communication_interface
        job.state = False
        messageBody = None
        # update circuit
        circuit.status = int(msgDict.get("status", circuit.status))
        circuit.credit = float(msgDict.get("cr", circuit.credit))
        session.merge(circuit)
        session.flush()
        if job._type == "addcredit":
            messageBody = make_message_body("credit.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin,
                                       status=circuit.get_rich_status(),
                                       credit=circuit.credit)
        elif job._type == "turnon" or job._type  == "turnoff":
            messageBody = make_message_body("toggle.txt",
                                       lang=circuit.account.lang,
                                       account=circuit.pin,
                                       status=circuit.get_rich_status(),
                                       credit=circuit.credit)
        # double to check we have a message to send
        if messageBody and originMsg:
            interface.sendMessage(
                originMsg.number,
                messageBody,
                incoming=originMsg.uuid)
        session.merge(job)
    else:
        pass


def make_pp(message, circuit, session):
    if valid(message.keys(),
             ['status', 'cid', 'tu', 'mid', 'wh', 'job']):
        date = parser.parse(message["ts"])
        log = PrimaryLog(
            date=date,
            circuit=circuit,
            watthours=message["wh"],
            use_time=message["tu"],
            credit=message.get("cr"),
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


def make_nocw(message, circuit, session):
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("nocw-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)
    session.flush()
    log = SystemLog(
        "Low credit alert for circuit %s sent to %s" % (circuit.pin,
                                                        circuit.account.phone))
    session.add(log)


def make_lcw(message, circuit, session):
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("lcw-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)
    session.flush()


def make_md(message, circuit, session):
    log = SystemLog(
        "Meter %s just falied, please investagte." % circuit.meter.name)
    session.add(log)


def make_ce(message, circuit, session):
    log = SystemLog(
        "Circuit %s just failed, please investagate." % circuit.ip_address)
    session.add(log)


def make_pmax(message, circuit, session):
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("power-max-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)


def make_emax(message, circuit, session):
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("energy-max-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)


def make_sdc(message, circuit, session):
    pass
