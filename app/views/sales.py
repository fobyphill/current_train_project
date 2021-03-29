from django.db.models import Sum, Count
from django.shortcuts import render, HttpResponseRedirect, reverse
import json
from app.models import Item, ItemTransfer, Transfer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json



def index(request):
    items = Item.objects.filter(is_active=True)[:150]
    # Если сессия пуста - создадим ее
    if not 'cart_items' in request.session:
        request.session['cart_items'] = []
    # принимаю товар в корзину
    if 'cart_item' in request.GET:
        cart_item = json.loads(request.GET['cart_item'])
        request.session['cart_items'].append(cart_item)
    paginator = Paginator(items, 10)
    if 'page' in request.GET:
        page_num = int(request.GET['page'])
    else:
        page_num = 1
    try:
        items_pages = paginator.page(page_num)
    except PageNotAnInteger:
        items_pages = paginator.page(1)
    except EmptyPage:
        items_pages = paginator.page(paginator.num_pages)


    ctx = {
        'title': 'Sales',
        # пагинаторский блок
        'items': items_pages,
        'pages_count': paginator.num_pages,
        'page_num': page_num,
    }
    return render(request, 'sales/index.html', ctx)

def order_view(request):
    if request.method == "POST":
        transfer = Transfer.objects.create(user_id=555, )  # Создали заказ
        q = ''
        t = ''
        item_id = ''  # временные переменные для количества, стоимости и  айди товара
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                if key[len(key) - 5:] == 'total':
                    t = request.POST[key]
                else:
                    q = request.POST[key]
                    item_id = key
                if t != '' and q != '':
                    ItemTransfer.objects.create(quantity=int(q), item_id=int(item_id),
                                                transfer_id=int(transfer.id), total=float(t))  # добавили количество и ид товаров
                    q = '';
                    t = '';
                    item_id = ''
        zakaz = Transfer.objects.filter(id=transfer.id).annotate(tot=Sum('itemtransfer__total'))
        return render(request, 'sales/my_order.html', context={'order_id': transfer.id})
    else:
        return HttpResponseRedirect(reverse("index"))
