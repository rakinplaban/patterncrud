from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Item
from .forms import ItemForm

# Create your views here.

def Index(request):
    
    item_list = Item.objects.all()
    
    if request.method == 'POST':
        form = ItemForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(request.path_info)
        else:
            form = ItemForm()
            return redirect(request.path_info)
    
    else:
        context = {
            'item_list': item_list
        }
        return render(request, 'index.html', context)


def item_create(request):
    
    data = dict()

    if request.method == 'POST':
        
        form = ItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            item_list = Item.objects.all()
            context = {
                'item_list': item_list
            }

            data['valid'] = True
            data['success'] = render_to_string('success/create-success.html')
            data['item_list'] = render_to_string('items/item_list.html', context)
            return JsonResponse(data)
        
        else:
            data['html_form'] = render_to_string('items/item_create.html')
            return JsonResponse(data)

    else:
        data['html_form'] = render_to_string('items/item_create.html')
        return JsonResponse(data)


def item_edit(request, id):
    
    data = dict()
    
    item = Item.objects.get(id=id)
    
    item_dic = {
        'item': item
    }

    if request.method == 'POST':
        
        form = ItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()
            
            item_list = Item.objects.all()
            context = {
                'item_list': item_list
            }

            data['valid'] = True
            data['success'] = render_to_string('success/edit-success.html')
            data['item_list'] = render_to_string('items/item_list.html', context)
            return JsonResponse(data)
        
        else:
            data['edit_form'] = render_to_string('items/item_edit.html', item_dic)
            return JsonResponse(data)
    
    else:
        data['edit_form'] = render_to_string('items/item_edit.html', item_dic)
        return JsonResponse(data)


def item_delete(request, id):
    
    data = dict()

    item = Item.objects.get(id=id)
    
    item_dic = {
        'item': item
    }

    if request.method == 'POST':
        
        item.delete()
        
        item_list = Item.objects.all()
        context = {
            'item_list': item_list
        }

        data['valid'] = True
        data['success'] = render_to_string('success/delete-success.html')
        data['item_list'] = render_to_string('items/item_list.html', context)
        return JsonResponse(data)
    
    else:
        data['delete_form'] = render_to_string('items/item_delete.html', item_dic)
        return JsonResponse(data)

