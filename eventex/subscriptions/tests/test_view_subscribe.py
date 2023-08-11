from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm
from django.conf import settings 
# Create your tests here.

class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
    
    def test_get(self):
        """Get / must return status code 200."""
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        """Must Use 'subscriptions/subscription_form.html' as the response's template."""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
    
    def test_html(self):
        """HTML MUST CONTAIN INPUT TAGS"""
        tags = (
            ('<form',1),
            ('<input',6),
            ('type="text"',3),
            ('type="email"',1),
            ('type="submit"',1)
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)
       
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos',cpf='12345678901', email='henrique@bastos.net', phone='21-99618-6180')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
        self.default_gmail = settings.DEFAULT_FROM_EMAIL

    def test_post(self):
        self.assertEqual(302, self.response.status_code)
    
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/',{})
        self.form = self.response.context['form']
    
    def test_post(self):
        self.assertEqual(200, self.response.status_code)
    
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
    
    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)
    
    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)

class SubscribeSucessMessage(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos',cpf='12345678901', email='henrique@bastos.net', phone='21-99618-6180')
        self.response = self.client.post('/inscricao/', data, follow=True)
    
    def test_message(self):
        self.assertContains(self.response, 'Inscrição Realizada com Sucesso!')