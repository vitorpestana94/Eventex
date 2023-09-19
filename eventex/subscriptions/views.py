from django.shortcuts import render
from django.core import mail
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
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


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404
        
    return render(request, 
                  'subscriptions/subscription_detail.html',
                  {'subscription': subscription})

def _success(request, form):
    subscription = Subscription.objects.create(**form.cleaned_data)
    _send_mail('confirmação de inscrição',settings.DEFAULT_FROM_EMAIL, 
               subscription.email, 
               'subscriptions/subscription_email.txt', 
               {'subscription': subscription})
    
    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))