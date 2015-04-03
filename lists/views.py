from django.shortcuts import render, redirect
# from django.http import HttpResponse
from lists.models import Item, List


def home_page(request):

    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        # return render(request, 'home.html', {'new_item_text': new_item_text})
        return redirect('/lists/the-only-list/')

    # items = Item.objects.all()
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html',
                  {'list': list_}
                  )


def new_list(request):
    if request.method == 'POST':
        item_text = request.POST['item_text']
        list_ = List.objects.create()
        Item.objects.create(text=item_text, list=list_)
        return redirect('/lists/%d/' % (list_.id,))

    return render(request, 'list.html')


def display_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html',
                  {'list': list_}
                  )


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
