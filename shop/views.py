from django.shortcuts import render
from django.contrib import messages


def Home(request):
    messages.info(request, 'Test Toast')
    return render(request, 'index.html')
