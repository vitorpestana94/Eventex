from django.shortcuts import render
from django.core import mail
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib import messages
from eventex.subscriptions.forms import SubscriptionForm
from django.conf import settings
# Create your views here.

def subscribe(request):
    return create(request) if request.method == 'POST' else new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    return render(request, 'subscriptions/subscription_form.html', {'form':form})  if not form.is_valid() else _success(request, form)
    

def new(request):
    return render(request,  'subscriptions/subscription_form.html', {'form':SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject,body, from_,[from_, to])


def _success(request, form):
    _send_mail('confirmação de inscrição',settings.DEFAULT_FROM_EMAIL, 
               form.cleaned_data['email'], 
               'subscriptions/subscription_email.txt', 
               form.cleaned_data)
    
    messages.success(request, 'Inscrição Realizada com Sucesso!')
    
    return HttpResponseRedirect('/inscricao/')