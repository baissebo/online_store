from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.text import slugify

from catalog.forms import ProductForm, ContactForm
from catalog.models import Product, Contact, BlogPost


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'latest_products'
    order_by = '-created_at'
    queryset = Product.objects.order_by('-created_at')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_products = self.object_list

        for product in latest_products:
            print(f"Название: {product.name}")
            print(f"Описание: {product.description}")
            print(f"Цена: {product.price}")
            print(f"Дата создания: {product.created_at}")
            print()

        return context


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = '/contacts/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    paginate_by = 5


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:product_detail')

    def form_valid(self, form):
        product = form.save()
        return redirect('catalog:product_detail', product.pk)


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogposts'
    paginate_by = 10


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'blogpost'


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ("title", "content", "preview_image", "is_published")
    template_name = 'catalog/blogpost_form.html'
    success_url = reverse_lazy('catalog:blogpost_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ("title", "content", "preview_image", "is_published")
    template_name = 'catalog/blogpost_form.html'
    context_object_name = 'blogposts'
    success_url = reverse_lazy('catalog:blogpost_list')


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('catalog:blogpost_list')
