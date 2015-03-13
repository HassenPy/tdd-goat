from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):

    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        # return render(request, 'home.html', {'new_item_text': new_item_text})
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html',
                  {'items_list': items}
                  )
