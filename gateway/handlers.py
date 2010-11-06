import transaction

from pyramid.view import action
from gateway.models import DBSession, Meter

class DashboardHandler(object):
    def __init__(self, request):
        self.request = request

    @action(renderer='index.mako')
    def index(self):
        session  = DBSession()  
        meters = session.query(Meter)
        return dict(meters=meters)
