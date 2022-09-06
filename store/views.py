from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from category.models import Category
from store.models import Product


def listing(request, products):
    paginator = Paginator(products, 6)
    page = request.GET.get('page', 1)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
    products_count = products.count()

    context = {
        'products': page_object,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


def shop(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    return listing(request, products)


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


def search(request):
    products = None
    if 'keyword' in request.GET:
        print('keyword')
        keyword = request.GET['keyword']
        print(keyword)
        if keyword:
            products = Product.objects.order_by('id')\
                .filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    return listing(request, products)
