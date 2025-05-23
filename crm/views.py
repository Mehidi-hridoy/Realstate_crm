from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, 'crm/base.html')

def index(request):
    return render(request, 'crm/index.html')    

def about(request):
    return render(request, 'crm/about.html')