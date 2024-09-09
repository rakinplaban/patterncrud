from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Item
from .forms import ItemForm
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    
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
            
            # Fetch the updated item list
            item_list = Item.objects.all()
            context = {
                'item_list': item_list
            }

            data['valid'] = True
            data['success'] = render_to_string('success/create-success.html', context)
            data['item_list'] = render_to_string('item/item_list.html', context)
            return JsonResponse(data)
        
        else:
            # Include form errors in the response
            data['html_form'] = render_to_string('item/item_create.html', {'form': form}, request=request)
            return JsonResponse(data)

    else:
        # Render the form for the first time
        data['html_form'] = render_to_string('item/item_create.html', {'form': ItemForm()}, request=request)
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
            data['item_list'] = render_to_string('item/item_list.html', context)
            return JsonResponse(data)
        
        else:
            data['edit_form'] = render_to_string('item/item_edit.html', item_dic)
            return JsonResponse(data)
    
    else:
        data['edit_form'] = render_to_string('item/item_edit.html', item_dic)
        return JsonResponse(data)


def item_delete(request, id):
    data = dict()
    item = get_object_or_404(Item, id=id)  # Use get_object_or_404 for better error handling
    
    if request.method == 'POST':
        item.delete()
        item_list = Item.objects.all()
        context = {'item_list': item_list}
        data['valid'] = True
        data['success'] = render_to_string('success/delete-success.html')
        data['item_list'] = render_to_string('item/item_list.html', context)
        return JsonResponse(data)
    else:
        context = {'item': item}
        data['delete_form'] = render_to_string('item/item_delete.html', context, request=request)
        return JsonResponse(data)