from django.shortcuts import render
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
