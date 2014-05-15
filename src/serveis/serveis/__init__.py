from pyramid.config import Configurator
from pyramid.renderers import JSONP
from pyramid.session import UnencryptedCookieSessionFactoryConfig

import os
here = os.path.dirname(os.path.abspath(__file__))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['mako.directories'] = os.path.join(here, 'templates')
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    config = Configurator( settings=settings, session_factory=my_session_factory )
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # general
    config.add_route('home', '/')
    config.add_route('jsontest', '/jsontest')
    
    # JsonXat
    config.add_route('xat_get_canals_ws', '/xat_get_canals_ws')
    config.add_route('xat_get_canal_ws', '/xat_get_canal_ws')
    config.add_route('xat_set_missatge_ws', '/xat_set_missatge_ws')
    
    config.scan()
    return config.make_wsgi_app()
