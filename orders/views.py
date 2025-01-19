from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet


def order_list(request):
    search_query = request.GET.get('search', '')
    order_status = request.GET.get('status', '')
    if search_query and order_status:
        orders = Order.objects.filter(order_id__icontains=search_query, status=order_status)
    elif search_query:
        orders = Order.objects.filter(order_id__icontains=search_query)
    elif order_status:
        orders = Order.objects.filter(status=order_status)
    else:
        orders = Order.objects.all()
    return render(request, 'orders/list.html', {'orders': orders})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        item_formset = OrderItemFormSet(request.POST)
        if form.is_valid() and item_formset.is_valid():
            order = Order.objects.create(
                order_id=form.cleaned_data['order_id'],
                order_date=form.cleaned_data['order_date'],
                order_status=form.cleaned_data['order_status'],
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                customer_phone=form.cleaned_data['customer_phone'],
                customer_address=form.cleaned_data['customer_address'],
            )
            item_formset.instance = order
            item_formset.save()
            messages.success(request, 'Order created successfully!')
            return redirect('orders:list')
        else:
            messages.error(request, 'There was an error creating the order. Please try again.')
    else:
        form = OrderForm()
        item_formset = OrderItemFormSet()

    return render(request, 'orders/form.html', {'form': form, 'item_formset': item_formset})


def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        item_formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and item_formset.is_valid():
            order.order_id = form.cleaned_data['order_id']
            order.order_date = form.cleaned_data['order_date']
            order.order_status = form.cleaned_data['order_status']
            order.customer_name = form.cleaned_data['customer_name']
            order.customer_email = form.cleaned_data['customer_email']
            order.customer_phone = form.cleaned_data['customer_phone']
            order.customer_address = form.cleaned_data['customer_address']
            order.save()
            item_formset.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('orders:list')
        else:
            messages.error(request, 'There was an error updating the order. Please try again.')
    else:
        form = OrderForm(initial={
            'order_id': order.order_id,
            'order_date': order.order_date,
            'order_status': order.order_status,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'customer_phone': order.customer_phone,
            'customer_address': order.customer_address,
        })
        item_formset = OrderItemFormSet(instance=order)

    return render(request, 'orders/form.html', {'form': form, 'item_formset': item_formset})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/detail.html', {'order': order})
