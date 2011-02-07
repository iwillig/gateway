"""
Forms for the Gateway web interface
"""
from webob.exc import HTTPFound
from colander import Mapping
from colander import SchemaNode
from colander import String
from colander import Integer
from colander import Date
from colander import Boolean
from deform import Form
from deform import ValidationFailure
from deform import widget
from deform import Button
from pyramid.security import authenticated_userid

from gateway.models import DBSession

matching = {'INTEGER': Integer,
            'STRING': String,
            'VARCHAR': String,
            'BOOLEAN': Boolean,
            'DATETIME': Date }


def form_route(handler, cls, **kwargs):
    """
    """
    schema = make_schema(cls,
                         excludes=kwargs.get('exludes', []))
    breadcrumbs = kwargs.pop('breadcrumbs')
    button = Button(*kwargs.get('buttons', ['Submit', 'Submit']))
    form = Form(schema, buttons=(button,))
    if handler.request.method == 'POST':
        controls = handler.request.POST.items()
        try:
            data = form.validate(controls)
            model = cls(**data)
            handler.session.add(model)
            handler.session.flush()
            return HTTPFound(
                location='%s%s' % (handler.request.application_url,
                                   model.getUrl()))
        except ValidationFailure, e:
            return {'form': e,
                    'breadcrumbs': breadcrumbs}
    return {'form': form,
            'class': cls,
            "logged_in": authenticated_userid(handler.request),
            'breadcrumbs': breadcrumbs}


def make_columns(cls):
    """
    Function to look up and convert a SQL types to a colander type
    Requires a Class the inherents from Base
    """
    session = DBSession()
    data = cls.__mapper__.columns._data
    columns = {}
    for key in data.keys():
        column = data[key]
        if len(column.foreign_keys) == 0:
            columns[key] = matching.get(
                str(column.type),
                String)
        elif len(column.foreign_keys) == 1:
            foregin = column.foreign_keys[0]
            table = foregin.column.table
            choices = session.query(table).all()
            columns[key] = [table, choices]
    return columns


def make_schema(cls, **kwargs):
    """
    Requires a class
    Returns a colander schema
    """
    schema = SchemaNode(Mapping())
    columns = make_columns(cls)
    map(lambda elem: columns.pop(elem), kwargs.get('excludes', []))
    # remove the id from the form
    columns.pop('id')
    if 'type' in columns.keys():
        columns.pop('type')
    if 'uuid' in columns.keys():
        columns.pop('uuid')
    for k, v in columns.iteritems():
        if isinstance(v, list):
            values = []
            for elem in v[1]:
                values.append((elem[1], elem[2]))
            schema.add(SchemaNode(
                String(),
                widget=widget.SelectWidget(values=values),
                name=k
                ))
        else:
            schema.add(SchemaNode(v(), name=k))
    return schema
