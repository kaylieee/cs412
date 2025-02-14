from django.shortcuts import render
import random
import time

# Create your views here.
def main(request):
    '''
    Define a view to handle the 'quote' request.
    '''

    template_name = 'restaurant/main.html'
    
    return render(request, template_name)

def order(request):
    '''
    Define a view to handle the 'order' request.
    '''
    specials = ['Spaghetti and Meatballs', 'Mushroom Risotto', 'Seasonal Veggie Pizza']
    rand_special = specials[random.randint(0, len(specials)-1)]
    special_desc = {
        'Spaghetti and Meatballs': 'Homemade spaghetti and meatballs',
        'Mushroom Risotto': 'Wild mushroom risotto with truffles',
        'Seasonal Veggie Pizza': 'Veggies bought fresh daily',
    }

    context = {
        'special': rand_special,
        'description': special_desc.get(rand_special),
    }

    template_name = 'restaurant/order.html'
    
    return render(request, template_name, context)

def confirmation(request):
    '''
    Define a view to handle the 'confirmation' request.
    '''

    template_name = "restaurant/confirmation.html"

    # read the form data into python variables:
    if request.POST:

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        instr = request.POST['instr']

        items = {
            'alfredo': ['Chicken Alfredo', 15],
            'pizza': ['Pepperoni Pizza', 10],
            'bread': ['Garlic Bread', 15],
            'soup': ['Italian Wedding Soup', 5],
        }

        total = 0
        ordered = []
        for order in request.POST.getlist('order'):
            if items.get(order):
                ordered.append(items.get(order)[0])
                total += items.get(order)[1]
            else:
                #ordered special
                ordered.append(order)
                total += 15
            
        prepTime = random.randint(30, 60)
        readyTime = time.ctime(time.time() + (prepTime*60))
        
        
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'instr': instr,
            'ordered': ordered,
            'total': total,
            'ready': readyTime,
            'extras': request.POST.getlist('extra')
        }
            

    return render(request, template_name, context=context)