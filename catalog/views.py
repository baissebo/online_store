from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.text import slugify

from catalog.forms import ProductForm, ContactForm, VersionForm, BaseVersionInlineFormSet, ProductModeratorForm, \
    BlogPostForm
from catalog.models import Product, Contact, BlogPost, Version
from catalog.services import get_categories_cache
from catalog.utils.congratulate_by_mail import congratulate_by_mail


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
        print(f'Имя: {name} Телефон: {phone} Сообщение: {message}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    paginate_by = 5

    def get_queryset(self):
        products = Product.objects.order_by('-created_at')

        for product in products:
            product.current_version = Version.objects.filter(product=product, is_current=True).first()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = get_categories_cache()
        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_detail')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return redirect('catalog:product_detail', product.pk)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, BaseVersionInlineFormSet, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            if formset.has_changed():
                formset.instance = self.object
                formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_edit_category") and user.has_perm("catalog.can_edit_description"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogposts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        congratulate_by_mail(obj)
        return obj


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ("title", "content", "preview_image", "is_published")
    template_name = 'catalog/blogpost_form.html'
    success_url = reverse_lazy('catalog:blogpost_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("catalog:blogpost_detail", args=[self.object.pk])


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ("title", "content", "preview_image", "is_published")
    template_name = 'catalog/blogpost_form.html'
    context_object_name = 'blogpost'
    success_url = reverse_lazy('catalog:blogpost_detail')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("catalog:blogpost_detail", args=[self.object.pk])

    def get_form_class(self):
        user = self.request.user

        if user == self.object.author or user.has_perms(["catalog.change_blogpost"]):
            return BlogPostForm
        raise PermissionDenied


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('catalog:blogpost_list')
