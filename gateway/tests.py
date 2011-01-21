import unittest
from sqlalchemy.orm.query import Query
from webob.exc import HTTPFound
from pyramid import testing


class GatewayTests(unittest.TestCase):
    """ Unit tests for the Gateway UI """
    def setUp(self):
        from pyramid.config import Configurator
        from gateway.models import initialize_sql
        self.session = initialize_sql('sqlite://')
        self.config = Configurator(autocommit=True)
        self.config.begin()
        from gateway.models import DBSession
        self.session = DBSession()

    def tearDown(self):
        self.config.end()

    def testDashboardIndex(self):
        request = testing.DummyRequest()
        from gateway.handlers import Dashboard
        handler = Dashboard(request)
        # test index
        index = handler.index()
        self.assertEqual(type(index['system_logs']), list)
        self.assertEqual(type(index['tokenBatchs']), list)
        self.assertEqual(type(index['breadcrumbs']), list)
        self.assertEqual(type(index['meters']), Query)

        add = handler.add_meter()
        self.assertEqual(type(add['breadcrumbs']), list)
        self.assertEqual(add['breadcrumbs'][1]['text'], 'Add a new meter')

        send_msg = handler.send_message()
        self.assertEqual(type(send_msg), HTTPFound)
        self.assertEqual(send_msg.status, '302 Found')

    def testUser(self):
        request = testing.DummyRequest()
        from gateway.handlers import UserHandler
        handler = UserHandler(request)

        # test login
        login = handler.login()
        self.assertEqual(login['url'], 'http://example.com/login',)
        self.assertEqual(login['login'], '')
        self.assertEqual(login['password'], '')
        self.assertEqual(login['came_from'], None)

        logout = handler.logout()
        self.assertEqual(type(logout), HTTPFound)
        self.assertEqual(logout.status, '302 Found')

    def testMeterHandler(self):
        from gateway.handlers import MeterHandler
        from gateway.models import Meter
        meter = Meter(name='test1001',
                      phone='18182124554',
                      location='New York City',
                      battery=12,
                      communication='gsm',
                      panel_capacity=10)
        self.session.add(meter)
        self.session.flush()
        request = testing.DummyRequest(path='http://example.com/meter/view/%s' % meter.uuid)
        handler = MeterHandler(request)
        # test meter index
        handler.index()


class GatewayNetbook(unittest.TestCase):
    """Test the netbook urls """
