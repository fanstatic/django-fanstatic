import re
from django.test import TestCase

class ResourceTests(TestCase):
    def test_static_resource(self):
        response = self.client.get('/')
        print response.content

    def test_implied_image(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        img_match = re.search('<img[^/]+src="(?P<url>[^"]+)"[^/]+/>',response.content)
        self.assertTrue(img_match is not None)
        img_url = img_match.group("url")
        response = self.client.get(img_url)
        self.assertEqual(response.status_code,200)
        self.assertTrue(len(response.content)>0)
        

