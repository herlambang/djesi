from django.conf import settings

"""
this middleware check if response has ESI tag (<esi:include...) and ESI is enabled, 
then it should initialize Surrogate-Control header.

why?
in varnish configuration, do_esi should enabled only with request that requires it
not all request need this header
"""
class DjangoEsiMiddleware(object):

    def process_response(self, request, response):
        if getattr(settings, 'USE_ESI', settings.DEBUG):
            if '<esi:include' in response.content:
                response['Surrogate-Control'] = 'ESI/1.0'
        return response
