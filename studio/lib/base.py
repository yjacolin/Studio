"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons.i18n.translation import set_lang, LanguageError
from pylons import session

from studio.model import meta

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            if 'lang' in session:
                try:
                    set_lang(session['lang'])
                except LanguageError:
                    # remove lang from session if an error occured
                    del session['lang']
                    session.save()

            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
        
