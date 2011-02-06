"""
Util functions that needed a better home
"""
import os
from collections import defaultdict
from mako.template import Template
from datetime import timedelta
from gateway.models import PrimaryLog


baseTemplate = "%s/gateway/templates/messages" % os.getcwd()


def nice_print(model):
    """Function for printing  """
    collector = {}
    modelDict = model.__dict__
    for k, v in modelDict.iteritems():
        if isinstance(v, object):
            collector.update({k: str(v)})
        else:
            collector.update({k: v})
    collector.pop('_sa_instance_state')
    return collector


def raise_first_leter(word):
    word = word[0].upper() + word[1:]
    return word.replace("_", " ")


def get_fields(model):
    """Takes a model and returns a useful dict"""
    fields = {}
    mapper = model.__mapper__
    columns = mapper.columns
    for key in columns.keys():
        field = columns.get(key).name
        niceName = raise_first_leter(field)
        fields.update({niceName.replace('_', ' '):
                        {"value": unicode(model.__getattribute__(field)),
                         "name": field,
                         "type": "input"}})
    return fields


class Widget(object):
    """
    """
    def __init__(self, iterable):
        """
        """
        self.iterable = iterable
        self.headers = self.make_header()

    def _header_as_th(self):
        thHtml = map(lambda header: "<th>%s</th>" % raise_first_leter(header),
                   self.headers)
        return "<thead>%s</thead>" % "".join(thHtml)

    def _iter_as_td(self, elem):
        return "<td>%s</td>" % elem

    def _iters_as_tbody(self):
        trHtml = []
        for elem in self.iterable:
            tds = []
            for k, v in get_fields(elem).iteritems():
                tds.append(self._iter_as_td(v.get("value")))
            trHtml.append("<tr>%s</tr>" % "".join(tds))
        return "<tbody>%s<tbody>" % "".join(trHtml)

    def as_table(self):
        return "<table>%s%s</table>" % (self._header_as_th(),
                                      self._iters_as_tbody())

    def as_list(self):
        pass

    def make_header(self):
        if isinstance(self.iterable, list):
            if len(self.iterable) > 0:
                return get_fields(self.iterable[0]).keys()
            else:
                raise NameError("Not an iter")
        else:
            if self.iterable.count():
                return get_fields(self.iterable.first()).keys()
            else:
                return []


def make_message_body(template="error.txt", lang="fr", **kwargs):
    """Builds a template based on name and langauge with kwargs passed
    to the template..  Returns a template object
    """
    templateName = "%s/%s/%s" % (baseTemplate, lang, template)
    template = Template(filename=templateName).render(**kwargs)
    return template


def model_from_request(request, model):
    params = request.params
    keys = params.keys()
    keys.remove("submit")
    for key in keys:
        model.__setattr__(key, params.get(key))
    return model


def make_table_header(klass):
    fields = []
    keys = klass.__mapper__.columns.keys()
    for key in keys:
        fields.append({"id": key,
                        "name": raise_first_leter(key),
                        "field": key})
    return fields


def make_table_data(models):
    data = []
    for model in models:
        field = {}
        for key in model.__mapper__.columns.keys():
            field.update({key: str(model.__getattribute__(key))})
        data.append(field)
    return data


def find_meter_logs(meter=None, date=None, session=None, days=30):
    """
    Meter, Date, DBSession
    Returns all logs within 30 days of a given date
    """
    logs = defaultdict(list)
    day30 = date - timedelta(days)
    circuits = meter.get_circuits()
    logQuery = session.query(PrimaryLog).filter(PrimaryLog.created >= day30)
    for circuit in circuits:
        logs['circuit' + str(circuit.id)].extend([nice_print(x) for x in
                                 logQuery.filter_by(circuit=circuit)])
    return logs
