from django.test import TestCase

class ResourceTests(TestCase):
    def test_static_resource(self):
        response = self.client.get('/')
        print response.content



