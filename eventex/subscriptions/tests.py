from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.views import default_gmail 
# Create your tests here.

class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
    
    def test_get(self):
        """Get / must return status code 200."""
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        """Must Use 'subscriptions/subscription_form.html' as the response's template."""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
    
    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input',6)
        self.assertContains(self.response, 'type="text"',3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    
    def test_form_have_field(self):
        form=self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos',cpf='12345678901', email='henrique@bastos.net', phone='21-99618-6180')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
        self.default_gmail = default_gmail

    def test_post(self):
        self.assertEqual(302, self.response.status_code)
    
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))
    
    def test_subscription_email_subject(self):
        self.assertEqual('confirmação de inscrição', self.email.subject)
    
    def test_subscription_email_from(self):
        self.assertEqual(self.default_gmail, self.email.from_email)
    
    def test_subscription_email_to(self):
        self.assertEqual([self.default_gmail, 'henrique@bastos.net'], self.email.to)
    
    def test_subscription_email_body(self):
        self.assertIn('Henrique Bastos', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('henrique@bastos.net', self.email.body)
        self.assertIn('21-99618-6180', self.email.body)


class SubscribeInvalidPost(TestCase):
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