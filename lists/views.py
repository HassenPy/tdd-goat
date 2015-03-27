from django.shortcuts import render, redirect
# from django.http import HttpResponse
from lists.models import Item


def home_page(request):

    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        # return render(request, 'home.html', {'new_item_text': new_item_text})
        return redirect('/lists/the-only-list/')

    # items = Item.objects.all()
    return render(request, 'home.html')


def view_list(request):
    items_list = Item.objects.all()
    return render(request, 'list.html',
                  {'items_list': items_list}
                  )


def new_list(request):
    if request.method == 'POST':
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        return redirect('/lists/the-only-list/')

    return render(request, 'list.html')
