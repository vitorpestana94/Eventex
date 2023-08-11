from django.core import mail
from django.test import TestCase
from django.conf import settings

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos',cpf='12345678901', email='henrique@bastos.net', phone='21-99618-6180')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
        self.default_gmail = settings.DEFAULT_FROM_EMAIL
    
    def test_subscription_email_subject(self):
        self.assertEqual('confirmação de inscrição', self.email.subject)
    
    def test_subscription_email_from(self):
        self.assertEqual(self.default_gmail, self.email.from_email)
    
    def test_subscription_email_to(self):
        self.assertEqual([self.default_gmail, 'henrique@bastos.net'], self.email.to)
    
    def test_subscription_email_body(self):
        contents = ['Henrique Bastos',
                '12345678901',
                'henrique@bastos.net',
                '21-99618-6180']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
