from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import pyramid_handlers
from dispatch import Dispatcher
from gateway.messaging import findMeter


dispatcher = Dispatcher()
dispatcher.addMatcher(findMeter,
                      'gateway.messaging.parse_meter_message')
dispatcher.addMatcher(r'^(bal).(\w+)',
                      'gateway.consumer.get_balance', langauge='en')
dispatcher.addMatcher(r'^(solde).(\w+)',
                      'gateway.consumer.get_balance', langauge='fr')
dispatcher.addMatcher(r'^(add).(\w+).(\d+)',
                      'gateway.consumer.add_credit',langauge='en')
dispatcher.addMatcher(r'^(recharge).(\w+).(\d+)',
                      'gateway.consumer.add_credit',langauge='fr')
dispatcher.addMatcher(r'^(on).(\w+)',
                      'gateway.consumer.turn_circuit_on', langauge='fr')
dispatcher.addMatcher(r'(off).(\w+)',
                      'gateway.consumer.turn_circuit_off', langauge='fr')
dispatcher.addMatcher(r'(prim).(\w+)',
                      'gateway.consumer.set_primary_contact',langauge='en')
dispatcher.addMatcher(r'(tel).(\w+)',
                      'gateway.consumer.set_primary_contact',langauge='fr')


def main(global_config, **settings):
    """ 
    This function returns a Pylons WSGI application.
    """
    from paste.deploy.converters import asbool
    from pyramid.config import Configurator
    from gateway.models import initialize_sql
    from gateway.security import groupfinder

    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application "
                         "configuration.")
    initialize_sql(db_string, asbool(settings.get('db_echo')))
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          autocommit=True,
                          root_factory='gateway.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.begin()
    session_factory = session_factory_from_settings(settings)
    config.include(pyramid_handlers.includeme)
    config.set_session_factory(session_factory)

    config.add_static_view('static','gateway:static/')
    config.add_static_view('deform-static', 'deform:static')

    config.add_handler('dashboard','/',
                       'gateway.handlers:Dashboard',
                       action='index')
    config.add_handler('main','/:action',
                      handler='gateway.handlers:Dashboard')
    config.add_handler('manage','/manage/:action',
                       handler='gateway.handlers:ManageHandler')
    config.add_handler('interfaces','/interface/:action/:interface',
                       handler='gateway.handlers:InterfaceHandler'),
    config.add_handler('export-load','sys/:action',
                       handler='gateway.sys:ExportLoadHandler')
    config.add_handler('kannel','kannel/:action',
                       handler='gateway.handlers:KannelHandler')
    config.add_handler('users','user/:action',
                      handler='gateway.handlers:UserHandler')
    config.add_handler('meter','meter/:action/:slug',
                       handler='gateway.handlers:MeterHandler') 
    config.add_handler('circuit','circuit/:action/:id',
                       handler='gateway.handlers:CircuitHandler')
    config.add_handler('logs','logs/:action/:meter/:circuit/',
                       handler='gateway.handlers:LoggingHandler') 
    config.add_handler('jobs','jobs/:action/:id/',
                       handler='gateway.handlers:JobHandler')
    config.add_handler('sms','sms/:action',
                       handler='gateway.handlers:SMSHandler') 
    config.add_handler('message','message/:action/:id',
                       handler='gateway.handlers:MessageHandler') 
    config.add_handler('account','account/:action/:id',
                       handler='gateway.handlers:AccountHandler')
    config.add_handler('token','token/:action/:id',
                       handler='gateway.handlers:TokenHandler')
    config.add_subscriber('gateway.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')
    config.end()
    return config.make_wsgi_app()
