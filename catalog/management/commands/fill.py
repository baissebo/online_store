from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('categories.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def json_read_products():
        with open('products.json', 'r') as f:
            return json.load(f)

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category_data in Command.json_read_categories():
            category = Category(pk=category_data['pk'],
                                name=category_data['fields']['name']
                                )
            category_for_create.append(category)

        Category.objects.bulk_create(category_for_create)

        for product_data in Command.json_read_products():
            product = Product(
                pk=product_data['pk'],
                name=product_data['fields']['name'],
                description=product_data['fields']['description'],
                image=product_data['fields']['image'],
                category=Category.objects.get(pk=product_data['fields']['category']),
                price=product_data['fields']['price'],
                created_at=product_data['fields']['created_at'],
                updated_at=product_data['fields']['updated_at']
            )
            product_for_create.append(product)

        Product.objects.bulk_create(product_for_create)
