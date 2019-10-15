from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse

class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')