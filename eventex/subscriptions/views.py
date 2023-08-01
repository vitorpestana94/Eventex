from django.shortcuts import render
from django.core import mail
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib import messages
from eventex.subscriptions.forms import SubscriptionForm
# Create your views here.

default_gmail = 'vitorpestanatr@gmail.com'

def subscribe(request):
    
    if request.method == 'POST':
        
        form = SubscriptionForm(request.POST)

        if form.is_valid():

            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
        
            mail.send_mail('confirmação de inscrição',body,default_gmail, [default_gmail, form.cleaned_data['email']]) 
            
            messages.success(request, 'Inscrição Realizada com Sucesso!')
            
            return HttpResponseRedirect('/inscricao/')
        
        else:
            
            return render(request, 'subscriptions/subscription_form.html', {'form':form})
    
    else:
        
        context = {'form': SubscriptionForm()}
        
        return  render(request, 'subscriptions/subscription_form.html', context)
