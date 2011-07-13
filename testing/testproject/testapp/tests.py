import re

from django.conf import settings
from django.test import TestCase


class ResourceTests(TestCase):

    def test_css(self):
        "Test the link injection for css done by fanstatic"
        response = self.client.get('/')

        # The index page should exist
        self.assertEqual(response.status_code, 200)

        # The injected link should be present (only once)
        css_match = re.search('<link[^>]+href="(?P<url>[^"]+)"[^/]+/>', response.content)
        self.assertEquals(len(css_match.groups()), 1)

        # The referred to css must exist
        css_url = css_match.group("url")
        response = self.client.get(css_url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response, '// a.css')

    def test_implied_image(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        img_match = re.search('<img[^/]+src="(?P<url>[^"]+)"[^/]+/>',response.content)
        self.assertTrue(img_match)
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

