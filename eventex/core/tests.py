from django.test import TestCase

# Create your tests here.
class HomeTest(TestCase):
    def test_get(self):
        """Get / must return status code 200"""
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
    
    def test_template(self):
        """Must use index.html"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "index.html")