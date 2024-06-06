from django.shortcuts import render, get_object_or_404, redirect

from catalog.forms import ProductForm
from catalog.models import Product, Contact


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]

    for product in latest_products:
        print(f"Название: {product.name}")
        print(f"Описание: {product.description}")
        print(f"Цена: {product.price}")
        print(f"Дата создания: {product.created_at}")

    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')

    contacts = Contact.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts})


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'products_list.html', context)


def products_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'products_details.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:products_details', product.pk)
    else:
        form = ProductForm()

        return render(request, 'create_product.html', {'form': form})
