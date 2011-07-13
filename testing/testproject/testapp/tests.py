import re
from django.test import TestCase

class ResourceTests(TestCase):
    def test_css(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        css_match = re.search('<link[^>]+href="(?P<url>[^"]+)"[^/]+/>',response.content)
        self.assertTrue(css_match is not None)
        css_url = css_match.group("url")


        # The css must be present
        response = self.client.get(css_url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response, '// a.css')

    def test_implied_image(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        img_match = re.search('<img[^/]+src="(?P<url>[^"]+)"[^/]+/>',response.content)
        self.assertTrue(img_match is not None)
        img_url = img_match.group("url")
        response = self.client.get(img_url)
        self.assertEqual(response.status_code,200)
        self.assertTrue(len(response.content)>0)
        

