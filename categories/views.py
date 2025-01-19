from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category
from orders.models import Order, OrderItem
from django.db.models import Sum
from django.db.models import Count
from .forms import CategoryForm
from django.utils import timezone


def home(request):
    total_sales = OrderItem.objects.aggregate(total_sales=Sum('price'))['total_sales']
    total_sales = total_sales if total_sales is not None else 0
    total_orders = Order.objects.count()
    last_month = timezone.now() - timezone.timedelta(days=30)
    new_customers = Order.objects.filter(order_date__gte=last_month).values('customer_name').distinct().count()
    products_by_category = OrderItem.objects.values('product__category__name').annotate(
        total_products=Count('product')).order_by('product__category__name')
    categories = [item['product__category__name'] for item in products_by_category]
    product_counts = [item['total_products'] for item in products_by_category]
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'new_customers': new_customers,
        'categories': categories,
        'product_counts': product_counts,
    }
    return render(request, 'index.html', context)


def category_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        categories = Category.objects.filter(name__icontains=search_query)
    else:
        categories = Category.objects.all()
    categories_with_count = []
    for category in categories:
        products_count = category.product_set.count()
        categories_with_count.append({
            'category': category,
            'products_count': products_count
        })
    context = {
        'categories_with_count': categories_with_count,
        'search_query': search_query,
    }
    return render(request, 'categories/list.html', context)


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            Category.objects.create(
                name=form.cleaned_data['name'],
                desc=form.cleaned_data['desc'],
                icon=form.cleaned_data['icon'],  # Save the icon here
            )
            messages.success(request, 'Category created successfully!')
            return redirect('categories:list')
        else:
            messages.error(request, 'There was an error submitting your form. Please try again.')
    else:
        form = CategoryForm()
    return render(request, 'categories/form.html', {'form': form})


def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            category.desc = form.cleaned_data['desc']
            category.icon = form.cleaned_data['icon']
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories:list')
    else:
        form = CategoryForm(initial={
            'name': category.name,
            'desc': category.desc,
            'icon': category.icon,
        })
    return render(request, 'categories/form.html', {'form': form})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'categories/detail.html', {'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('categories:list')
    return render(request, 'categories/delete-confirm.html', {'category': category})