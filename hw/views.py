from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time

# Create your views here.

def home(request):
    '''
    Define a view to handle the 'home' request.
    '''

    # response_text = '''
    # <html>
    # <h1>Hello, world!</h1>

    # </html>
    # '''
    
    # return HttpResponse(response_text)

    template_name = 'hw/home.html'
    context = {
        'time': time.ctime()
    }
    return render(request, template_name, context)