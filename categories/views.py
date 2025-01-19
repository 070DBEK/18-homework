from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category
from products.models import Product
from .forms import CategoryForm


def home(request):
    products_count = Product.objects.count()
    return render(request, 'index.html', {'products_count' : products_count})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/list.html', {'categories': categories})

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