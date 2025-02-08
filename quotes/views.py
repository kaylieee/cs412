from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.
quotes = [
    "Life is not easy for any of us. But what of that? We must have perseverance and above all confidence in ourselves. We must believe that we are gifted for something and that this thing must be attained.",
    "Nothing in life is to be feared; it is only to be understood.",
    "Have no fear of perfection; you'll never reach it.",
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Marie_Curie_c._1920s.jpg/440px-Marie_Curie_c._1920s.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/9/93/Marie_Curie_1903.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Irene_and_Marie_Curie_1925.jpg/360px-Irene_and_Marie_Curie_1925.jpg",
]

def quote(request):
    '''
    Define a view to handle the 'quote' request.
    '''

    rand_quote = quotes[random.randint(0, len(quotes)-1)]
    rand_image = images[random.randint(0, len(images)-1)]

    context = {
        'quote': rand_quote,
        'image': rand_image,
    }

    template_name = 'quote.html'
    
    return render(request, template_name, context)

def about(request):
    '''
    Define a view to handle the 'about' request.
    '''
    template_name = 'about.html'
    
    return render(request, template_name)

def show_all(request):
    '''
    Define a view to handle the 'show_all' request.
    '''
    context = {
        'quotes': quotes,
        'images': images,
    }

    template_name = 'show_all.html'
    return render(request, template_name, context)
