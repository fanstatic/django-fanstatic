import re

from django.conf import settings
from django.test import TestCase


class ResourceTests(TestCase):

    link_re = re.compile('<link[^>]+href="(?P<url>[^"]+)"[^/]+/>')
    img_re =  re.compile('<img[^/]+src="(?P<url>[^"]+)"[^/]+/>')


    def assert_css_file(self, css_url,signature):
        response = self.client.get(css_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, signature)

    def test_css(self):
        "Test the link injection for css done by fanstatic"
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        css_match = self.link_re.search(response.content)
        self.assertTrue(css_match is not None)
        css_url = css_match.group("url")
        
        # The css must be present
        self.assert_css_file(css_url,'/* a.css */')
        
    def test_error(self):
        """ test the cleaning of resources on exceptions """

        ### Django's standard client tries its best to expose internal application exception and
        ### therefore rethrows exception. For this error test we want to see the error template's result
        ### rather than the raised exception
        temp_error = self.client.store_exc_info
        def f(**kwargs):
            pass
        self.client.store_exc_info = f
        try:
            response = self.client.get('/error')
        finally:
            self.client.store_exc_info = temp_error
        self.assertEqual(response.status_code,500)
        links =list(self.link_re.finditer(response.content))
        self.assertEqual(len(links),1) # this means that exactly one css link was generated

        # now test it is error.css
        self.assert_css_file(links[0].group("url"),"/* error.css */")

    def test_implied_image(self):
        " test an undeclared image resource  "
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        img_match = self.img_re.search(response.content)
        self.assertTrue(img_match is not None)
        img_url = img_match.group("url")
        response = self.client.get(img_url)
        self.assertEqual(response.status_code,200)
        self.assertTrue(len(response.content)>0)

    def test_fanstatic_not_working_without_middleware(self):
        """
        Test that fanstatic doesn't do anything when the middleware is not
        installed in the MIDDLEWARE_CLASSES setting.
        """
        old_middleware = settings.MIDDLEWARE_CLASSES

        new_middleware = list(settings.MIDDLEWARE_CLASSES)
        new_middleware.remove('django_fanstatic.FanstaticMiddleware')
        settings.MIDDLEWARE_CLASSES = new_middleware

        # The index page should exist
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # The injected link should not be present (only once)
        css_match = re.search('<link[^>]+href="(?P<url>[^"]+)"[^/]+/>', response.content)
        self.assertFalse(css_match)

        settings.MIDDLEWARE_CLASSES = old_middleware

