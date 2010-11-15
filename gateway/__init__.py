from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """ This function returns a Pylons WSGI application.
    """
    from paste.deploy.converters import asbool
    from pyramid.configuration import Configurator
    from gateway.models import initialize_sql
    from gateway.security import groupfinder
    from gateway.messaging import process_messages

    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application "
                         "configuration.")
    initialize_sql(db_string, asbool(settings.get('db_echo')))
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          root_factory='gateway.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.begin()
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    config.add_static_view(
        'static',
        'gateway:static/'
        )
    config.add_handler('dashboard','/',
                       'gateway.handlers:Dashboard',
                       action='index')
    config.add_handler('main','/:action',
                      handler='gateway.handlers:Dashboard')
    config.add_handler('users','user/:action',
                      handler='gateway.handlers:UserHandler')
    config.add_handler('meter','meter/:action/:id',
                       handler='gateway.handlers:MeterHandler') 
    config.add_handler('circuit','circuit/:action/:id',
                       handler='gateway.handlers:CircuitHandler')
    config.add_handler('logs','logs/:action/:meter/:circuit/',
                       handler='gateway.handlers:LoggingHandler') 
    config.add_handler('alerts','alerts/:action/:meter/:circuit/',
                       handler="gateway.handlers:AlertHandler")
    config.add_handler('jobs','jobs/:action/:id/',
                       handler='gateway.handlers:JobHandler')
    config.add_handler('sms','sms/:action',
                       handler='gateway.handlers:SMSHandler') 
    config.add_handler('account','account/:action/:id',
                       handler='gateway.handlers:AccountHandler')
    config.add_handler('token','token/:action/:id',
                       handler='gateway.handlers:TokenHandler')
    config.add_subscriber('gateway.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')
    config.end()
    # start the thread
    process_messages.setDaemon(True) 
    process_messages.start() 
    return config.make_wsgi_app()
