from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib import messages
from django.shortcuts import render
from categories.models import Category


def product_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_id:
        products = products.filter(category_id=category_id)

    if sort_by == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_id': category_id,
        'sort_by': sort_by,
    }
    return render(request, 'products/list.html', context)


def create_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product.objects.create(
                name=form.cleaned_data['name'],
                desc=form.cleaned_data['desc'],
                img=form.cleaned_data['img'],
                price=form.cleaned_data['price'],
                category=form.cleaned_data['category'],
            )
            messages.success(request, 'Product created successfully!')
            return redirect('products:list')
        else:
            messages.error(request, 'There was an error submitting your form. Please try again.')
    else:
        form = ProductForm()
    return render(request, 'products/form.html', {'form': form})


def update_products(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.desc = form.cleaned_data['desc']
            product.price = form.cleaned_data['price']
            product.img = form.cleaned_data['img']
            product.category = form.cleaned_data['category']
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:list')
        else:
            messages.error(request, 'There was an error updating your product. Please try again.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/form.html', {'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:list')
    return render(request, 'products/delete-confirm.html', {'product': product})
