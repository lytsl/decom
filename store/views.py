from django.shortcuts import render, get_object_or_404

from category.models import Category
from store.models import Product


def shop(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    context = {
        'products': products[:10],
        'products_count': products_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        product = Product.objects.get(category=category, slug=product_slug)
        images = product.images.all()
    except Exception as e:
        raise e
    context = {
        'product': product,
        'category': category,
        'images': images,
    }
    return render(request, 'store/product_detail.html', context)
