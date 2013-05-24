import re

from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.template import Template, Context, RequestContext
from django.test.client import RequestFactory

# Create your tests here.

from djesi.middleware.esi import DjangoEsiMiddleware
from djesi.templatetags.djesi import esi

import mock

class MiddlewareTest(TestCase):

    def test_middleware_response_with_esi(self):
        settings.USE_ESI    = True
        
        middleware          = DjangoEsiMiddleware()
        response            = HttpResponse()
        response.content    = '<html><body><esi:include src="http://localhost/"/>'
        response            = middleware.process_response(None, response)
        self.assertTrue('Surrogate-Control' in response)
        self.assertEqual('ESI/1.0', response['Surrogate-Control'])
    
    def test_middleware_response_without_esi(self):
        settings.USE_ESI    = False
        
        middleware          = DjangoEsiMiddleware()
        response            = HttpResponse()
        response.content    = '<html><body><esi:include src="http://localhost/"/>'
        response            = middleware.process_response(None, response)
        self.assertFalse('Surrogate-Control' in response)



class TemplatetagsTest(TestCase):

    def setUp(self):
        request = RequestFactory()
        self.request = request.get('/')

    @staticmethod
    def fake_view(request, year, month):
        response = HttpResponse()
        response.content = 'fake content'
        return response

    @mock.patch('djesi.templatetags.djesi.resolve')
    @mock.patch('djesi.templatetags.djesi.reverse')
    def test_templatetag_without_ESI(self,mock_reverse, mock_resolve):
        settings.USE_ESI = False
        
        mock_reverse.return_value = '/hah/blah'
        mock_resolve.return_value = [TemplatetagsTest.fake_view, None, {}]
        
        context = {
            'request': self.request
        }
        content = esi(context, 'fake_view', year='2013', month='05')

        self.assertEqual(content, 'fake content')
        

    @mock.patch('djesi.templatetags.djesi.resolve')
    @mock.patch('djesi.templatetags.djesi.reverse')
    def test_templatetag_with_ESI(self,mock_reverse, mock_resolve):
        settings.USE_ESI = True
        
        mock_reverse.return_value = '/hah/blah'
        mock_resolve.return_value = [TemplatetagsTest.fake_view, None, {}]
        
        context = {
            'request': self.request
        }
        content = esi(context, 'fake_view', year='2013', month='05')

        regexp = re.compile(r'<esi:include src="http://.*/hah/blah"/>')
        self.assertTrue(regexp.search(content) is not None)


