"""
Handler objects of web interface
"""
import datetime
import csv
from urlparse import parse_qs
import uuid
import cStringIO
import simplejson
from dateutil import parser
from webob import Response
from webob.exc import HTTPFound
from pyramid_handlers import action
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget
from sqlalchemy import or_, desc
from deform import Form
from gateway import dispatcher
from gateway import models
from gateway.models import DBSession
from gateway.models import Meter
from gateway.models import Circuit
from gateway.models import PrimaryLog
from gateway.models import Job
from gateway.models import AddCredit
from gateway.models import Account
from gateway.models import TokenBatch
from gateway.models import Token
from gateway.models import Message
from gateway.models import IncomingMessage
from gateway.models import OutgoingMessage
from gateway.models import SystemLog
from gateway.models import Mping
from gateway.models import CommunicationInterface
from gateway.security import USERS
from gateway.utils import get_fields
from gateway.utils import model_from_request
from gateway.utils import make_table_header
from gateway.utils import make_table_data
from gateway.utils import find_meter_logs
from gateway.form import form_route
from gateway.form import TokenBatchSchema

breadcrumbs = [{"text":"Manage Home", "url":"/"}]


class Dashboard(object):
    """
    Home page for the gateway
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    @action(renderer='index.mako', permission="view")
    def index(self):
        batchSchema = TokenBatchSchema()
        batchForm = Form(batchSchema, buttons=('Add tokens',))
        meters = self.session.query(Meter)
        interfaces = self.session.query(CommunicationInterface).all()
        tokenBatchs = self.session.query(TokenBatch).all()
        system_logs = self.session.query(SystemLog).\
            order_by(desc(SystemLog.created)).all()
        return {
            'batchForm': batchForm,
            'interfaces': interfaces,
            'logged_in': authenticated_userid(self.request),
            'tokenBatchs': tokenBatchs,
            'system_logs': system_logs,
            'meters': meters,
            'breadcrumbs': self.breadcrumbs }

    @action(renderer="dashboard.mako", permission="admin")
    def dashboard(self):
        return {
            "logged_in": authenticated_userid(self.request),
            }

    @action(renderer="meter/add.mako", permission="admin")
    def add_meter(self):
        breadcrumbs = self.breadcrumbs
        breadcrumbs.append({"text": "Add a new meter"})
        return form_route(self,
                          Meter,
                          buttons=['add_meter', 'Add new circuit'],
                          exludes=['slug',
                                   'uuid',
                                   'date'],
                          breadcrumbs=breadcrumbs)

    @action(renderer='add_interface.mako', permission='admin')
    def add(self):
        _type = self.request.params.get('class')
        cls = getattr(models, _type)
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Add a new %s ' % _type})
        return form_route(self,
                          cls,
                          buttons=['submit', 'Add new %s' % _type],
                          breadcrumbs=breadcrumbs)

    @action(permission="admin")
    def add_tokens(self):
        self.request.params
        batch = TokenBatch()
        self.session.add(batch)
        amount = self.request.params.get("amount", 100)
        value = int(self.request.params.get("value", 10))
        for number in xrange(0, int(amount)):
            self.session.add(Token(
                    token=Token.get_random(),
                    value=value,
                    batch=batch))
        return HTTPFound(location=self.request.application_url)

    @action(permission="admin")
    def upload_tokens(self):
        csvReader = csv.reader(self.request.params['csv'].file, delimiter=',')
        batch = TokenBatch()
        self.session.add(batch)
        header = csvReader.next()
        for line in csvReader:
            self.session.add(Token(
                    token=line[1],
                    value=line[2],
                    batch=batch))
        return HTTPFound(location=self.request.application_url)

    @action()
    def system_logs(self):
        return Response(
            simplejson.dumps(
                [x.text for x in self.session.query(SystemLog).all()]))

    @action(permission="admin")
    def send_message(self):
        params = self.request.params
        msgClass = getattr(models, params['delivery-type'])
        msg = msgClass(
                number=params.get("number"),
                text=params.get("text"))
        self.session.add(msg)
        self.session.flush()
        return HTTPFound(location=self.request.application_url)


class ManageHandler(object):
    """
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer='manage/index.mako')
    def index(self):
        return {
            'logged_in': authenticated_userid(self.request),
            'breadcrumbs': self.breadcrumbs }


class UserHandler(object):

    def __init__(self, request):
        self.request = request

    @action(renderer="login.mako")
    def login(self):
        came_from = self.request.params.get('came_from',)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in self.request.params:
            login = self.request.params['login']
            password = self.request.params['password']
            if USERS.get(login) == password:
                headers = remember(self.request, login)
                return HTTPFound(location="/",
                                 headers=headers)
            message = 'Failed login'
        return {
            'message': message,
            'url': self.request.application_url + '/login',
            'came_from': came_from,
            'login': login,
            'password': password }

    def logout(self):
        headers = forget(self.request)
        return HTTPFound(
            headers=headers,
            location=self.request.application_url)


class InterfaceHandler(object):
    """
    A handler for managing the interfaces.
    """

    def __init__(self, request):
        self.breadcrumbs = breadcrumbs
        self.request = request
        self.session = DBSession()
        self.interface = self.session.query(
            CommunicationInterface).get(self.request.matchdict.get('id'))

    @action(renderer='interface/index.mako', permission='admin')
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Interface overview'})
        return {'interface': self.interface,
                'breadcrumbs': breadcrumbs,
                'fields': get_fields(self.interface),
                'logged_in': authenticated_userid(self.request)}

    def save_and_parse_message(self, origin, text, id=None):
        """
        Function to save incoming message based on relay type. Takes the
        message class, the numner, the body of the message and a
        session. Optional argument is the messages id. Parses the message
        and return the message object.
        """
        if id is None:
            id = str(uuid.uuid4())
        message = IncomingMessage(origin, text, id, self.interface)
        self.session.add(message)
        self.session.flush()
        dispatcher.matchMessage(message)
        return message

    @action()
    def send(self):
        msg = self.save_and_parse_message(self.request.params['number'],
                                          self.request.params['message'])
        return Response(msg.uuid)

    @action()
    def remove(self):
        self.session.delete(self.interface)
        self.session.flush()
        return HTTPFound(location="%s/" % self.request.application_url)


class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters
    """
    def __init__(self, request):
        self.request = request
        self.session  = DBSession()
        self.meter = self.session.query(Meter).\
                     filter_by(slug=self.request.matchdict['slug']).one()
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="meter/index.mako", permission="admin")
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text": "Meter Overview"})
        circuit_data = make_table_data(self.meter.get_circuits())
        return {
            "logged_in": authenticated_userid(self.request),
            "meter": self.meter,
            "circuit_header": make_table_header(Circuit),
            "circuit_data": circuit_data,
            "fields": get_fields(self.meter),
            "breadcrumbs": breadcrumbs }

    @action(request_method='POST', permission="admin")
    def add_circuit(self):
        params = self.request.params
        pin = params.get("pin")
        if len(pin) == 0:
            pin = Circuit.get_pin()
        account = Account(
            lang=params.get("lang"),
            phone=params.get("phone"))
        circuit = Circuit(meter=self.meter,
                          account=account,
                          pin=pin,
                          ip_address=params.get("ip_address"),
                          energy_max=int(params.get("energy_max")),
                          power_max=int(params.get("power_max")))
        self.session.add(account)
        self.session.add(circuit)
        self.session.flush()
        return HTTPFound(location="%s%s" % (
                self.request.application_url, self.meter.getUrl()))

    @action(renderer="meter/edit.mako", permission="admin")
    def edit(self):
        return {
            "fields": get_fields(self.meter),
            "meter": self.meter }

    @action(renderer="meter/build_graph.mako", permission="admin")
    def build_graph(self):
        return {
            "logged_in": authenticated_userid(self.request),
            "meter": self.meter }

    @action(renderer="meter/show_graph.mako", permission="admin")
    def show_graph(self):
        #needs to be implemented
        return {}

    @action(permission="admin")
    def logs(self):
        days = int(self.request.params.get('days', 10))
        date = datetime.now()
        logs = find_meter_logs(meter=self.meter,
                               date=date, session=self.session,
                               days=days)
        return Response(
            simplejson.dumps(logs),
            content_type='application/json')

    @action(permission="admin")
    def update(self):
        meter = model_from_request(self.request,
                                   self.meter)
        self.session.merge(meter)
        return HTTPFound(
            location="%s%s" % (self.request.application_url,
                               self.meter.getUrl()))

    @action(permission="admin")
    def remove(self):
        self.session.delete(self.meter)
        [self.session.delete(x)
         for x in self.session.query(Circuit).filter_by(meter=self.meter)]
        return HTTPFound(location="/")

    @action(permission="admin")
    def ping(self):
        job = Mping(self.meter)
        self.session.add(job)
        self.session.flush()
        msgClass = self.meter.getMessageType(job=True)
        self.session.add(msgClass(job, self.meter.phone, incoming=""))
        return HTTPFound(location=self.meter.getUrl())


class CircuitHandler(object):
    """
    Circuit handler. Has all of the most
    important urls for managing circuits
    """

    def __init__(self, request):
        self.session = DBSession()
        self.request = request
        self.circuit = self.session.\
                       query(Circuit).get(self.request.matchdict["id"])
        self.meter = self.circuit.meter
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="circuit/index.mako", permission="admin")
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.extend([
                    {"text": "Meter Overview", "url": self.meter.getUrl()},
                    {"text": "Circuit Overview"}])
        return {
            "logged_in": authenticated_userid(self.request),
            "breadcrumbs": breadcrumbs,
            "jobs": self.circuit.get_jobs(),
            "fields": get_fields(self.circuit),
            "circuit": self.circuit }

    @action(renderer="circuit/edit.mako", permission="admin")
    def edit(self):
        breadcrumbs = self.breadcrumbs
        breadcrumbs.extend([
                    {"text": "Meter Overview", "url": self.meter.getUrl()},
                    {"text": "Circuit Overview", "url": self.circuit.url()},
                    {"text": "Circuit Edit"}])
        return {
            "logged_in": authenticated_userid(self.request),
            "breadcrumbs": breadcrumbs,
            "fields": get_fields(self.circuit),
            "circuit": self.circuit }

    @action(permission="admin")
    def update(self):
        circuit = model_from_request(
            self.request, self.circuit)
        self.session.merge(circuit)
        return HTTPFound(
            location="%s%s" % (self.request.application_url,
                           self.circuit.getUrl()))

    @action(permission="admin")
    def turn_off(self):
        self.circuit.turnOff()
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def turn_on(self):
        self.circuit.turnOn()
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def ping(self):
        self.circuit.ping()
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def remove_jobs(self):
        [self.session.delete(job) for job in self.circuit.get_jobs()]
        return HTTPFound(
            location="%s%s" % (self.request.application_url,
                                self.circuit.getUrl()))

    @action(renderer="circuit/build_graph.mako", permission="admin")
    def build_graph(self):
        return {
            "logged_in": authenticated_userid(self.request),
            "circuit": self.circuit }

    @action(renderer="circuit/show_graph.mako", permission="admin")
    def show_graph(self):
        query = self.session.query(PrimaryLog)
        params = self.request.params
        # parse the date from the request
        origin = parser.parse(params["from"])
        to = parser.parse(params["to"])
        yaxis = params["yaxis"]
        logs = [x for x in query.all() if x.created > origin]
        logs = [x for x in logs if x.created < to]
        return {
            "logged_in": authenticated_userid(self.request),
            "data": [{"time": str(x.created.ctime()),
                      "value": x.get_property(yaxis)} for x in logs ],
            "y_units": simplejson.dumps(params["yaxis"]),
            "origin": simplejson.dumps(params["from"]),
            "to": simplejson.dumps(params["to"])}

    @action()
    def jobs(self):
        return Response([x.toJSON() for x in self.circuit.get_jobs()])

    @action(permission="admin")
    def add_credit(self):
        job = AddCredit(circuit=self.circuit,
                  credit=self.request.params.get("amount"))
        self.session.add(job)
        self.session.flush()
        msgClass = self.circuit.meter.getMessageType()
        self.session.add(msgClass(job, ""))
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def remove(self):
        self.session.delete(self.circuit)
        return HTTPFound(location=self.meter.getUrl())


class AccountHandler(object):
    """
    """

    def __init__(self, request):
        self.session = DBSession
        self.request = request
        self.account = self.session.\
            query(Account).get(self.request.matchdict.get("id"))

    def index(self):
        return Response(str(self.account))

    @action(renderer="account/edit.mako", permission="admin")
    def edit(self):
        return {"account": self.account,
                 "fields": get_fields(self.account)}

    @action(permission="admin")
    def update(self):
        account = model_from_request(self.request,
                                     self.account)
        self.session.add(account)
        return Response()


class LoggingHandler(object):

    def __init__(self, request):
        session = DBSession()
        self.request = request
        matchdict = self.request.matchdict
        circuit_id = matchdict["circuit"].replace("_", ".")
        self.meter = session.\
            query(Meter).filter_by(name=matchdict["meter"]).first()
        self.circuit = session.\
            query(Circuit).filter_by(ip_address=circuit_id).first()

    @action()
    def pp(self):
        """
        Primary log action. Should force the meter to provide authentication
        """
        params = parse_qs(self.request.body)
        session = DBSession()
        if not self.meter or not self.circuit:
            return Response(status=404)
        log = PrimaryLog(circuit=self.circuit,
                   watthours=params["wh"][0],
                   use_time=params["tu"][0],
                   credit=params["cr"][0],
                   status=int(params["status"][0]))
        self.circuit.credit = float(log.credit)
        self.circuit.status = int(params["status"][0])  # fix
        session.add(log)
        session.merge(self.circuit)
        return Response("ok")

    @action()
    def sp(self):
        return Response(self.request)


class JobHandler(object):

    def __init__(self, request):
        self.request = request

    @action()
    def meter(self):
        session = DBSession()
        matchdict = self.request.matchdict
        meter = session.query(Meter).filter_by(slug=matchdict["id"]).first()
        return Response("".join([str(x) for x in meter.getJobs()]))

    @action()
    def job(self):
        session = DBSession()
        job = session.query(Job).get(self.request.matchdict["id"])
        if self.request.method == "DELETE":
            job.state = False
            job.end = datetime.datetime.now()
            session.merge(job)
            return Response(job.toString())
        else:
            return Response(simplejson.dumps(job.toDict()))


class TokenHandler(object):

    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.batch = self.session.\
            query(TokenBatch).filter_by(
            uuid=self.request.matchdict["id"]).first()

    @action(permission="admin")
    def show_batch(self):
        return Response(simplejson.dumps(
                [x.toDict() for x in self.batch.get_tokens()]))

    @action(permission="admin")
    def export_batch(self):
        tokens = self.batch.get_tokens()
        s = cStringIO.StringIO()
        csvWriter = csv.writer(s)
        mapper = tokens[0].__mapper__
        csvWriter.writerow(mapper.columns.keys())
        csvWriter.writerows(map(
                lambda model:
                map(lambda k: getattr(model, k),
                    mapper.columns.keys()), tokens))
        s.reset()
        resp = Response(s.getvalue())
        resp.content_type = 'application/x-csv'
        resp.headers.add('Content-Disposition',
                         'attachment;filename=tokens.csv')
        return resp

    @action(permission="admin")
    def refresh(self):
        return Response("stuff")


class MessageHandler(object):
    def __init__(self, request):
        self.session = DBSession()
        self.request = request
        self.message = self.session.\
                       query(Message).filter_by(
            uuid=self.request.matchdict["id"]).first()

    @action(renderer='sms/index_msg.mako')
    def index(self):
        global breadcrumbs
        breadcrumbs.extend({})
        return {
            'breadcrumbs': breadcrumbs,
            'message': self.message }

    @action(request_method="POST")
    def remove(self):
        self.message.sent = True
        self.session.merge(self.message)
        return Response("ok")

    @action(renderer='sms/delete_msg.mako')
    def delete(self):
        if self.request.method == 'POST':
            return Response("Removed Message")
        elif self.request.method == 'GET':
            return {'message': self.message }


class SMSHandler(object):
    """
    Handler for most SMS operations
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    @action(renderer="sms/index.mako", permission="admin")
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text": "SMS Message"})
        limit = self.request.params.get('limit', 1000)
        count = self.session.query(Message).count()
        messages = self.session.\
            query(Message).order_by(desc(Message.id)).limit(limit)
        return {
            "logged_in": authenticated_userid(self.request),
            "limit": limit,
            "count": count,
            "messages": messages,
            "table_headers": make_table_header(OutgoingMessage),
            "breadcrumbs": breadcrumbs }

    @action(permission="admin")
    def remove_all(self):
        [self.session.delete(msg) for msg in self.session.query(Message).all()]
        return HTTPFound(
            location="%s/sms/index" % self.request.application_url)

    @action()
    def ping(self):
        return Response('ok')

    @action()
    def received(self):
        msgs = [msg.toDict() for msg in self.session.query(Message).\
                filter_by(sent=False).filter(or_(Message.type == "job_message",
                  Message.type == "outgoing_message")).all()
                  if msg.number != '']
        return Response(
            content_type="application/json",
            body=simplejson.dumps(msgs))
