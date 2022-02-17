from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from functools import reduce
import operator
from .models import Product, Category, Manufacturer, TyreSize

# Create your views here.

def all_products(request):
    """ A view to return all products page """

    products = Product.objects.all().order_by('price', 'name')
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all().order_by('display_name', )
    sizes = TyreSize.objects.all().order_by('rim_size', 'width',)

    query_search = None
    query_filter_season = None
    query_filter_size = None

    query_filter_brand = None

    sort = None
    direction = None



    if request.GET:
        # Handles free search bar functionality
        if 'q' in request.GET:
            query_search = request.GET['q']
            if not query_search:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(
                name__icontains=query_search) | Q(
                description__icontains=query_search) | Q(
                size__full_size_display__icontains=query_search) | Q(
                size__full_size_code__icontains=query_search) | Q(
                size__full_size_short__icontains=query_search)
            products = products.filter(queries)

        # Handles main filtering functionality
        if 'season' in request.GET:
            query_filter_season = request.GET['season']
            query_filter_size = request.GET['size']

            queries = Q(
                category__name__icontains=query_filter_season) & Q(
                size__full_size_code__icontains=query_filter_size)
            products = products.filter(queries)

        if 'season' and 'brand' in request.GET:
            query_filter_season = request.GET['season']
            query_filter_size = request.GET['size']
            query_filter_brand = request.GET.getlist('brand')
            print(query_filter_brand)
  
            queries = Q(
                category__name__icontains=query_filter_season) & Q(
                size__full_size_code__icontains=query_filter_size)
            query_brand = reduce(operator.or_, (Q(
                manufacturer__name__icontains=each_brand
                ) for each_brand in query_filter_brand))
            print(query_brand)
            products = products.filter(queries).filter(query_brand)

        # Handles sorting functionality
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    selected_sort_method = f'{sort}_{direction}'

    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'sizes': sizes,
        'search_term': query_search,
        'filter_term_season': query_filter_season,
        'filter_term_size': query_filter_size,
        'filter_term_brand': query_filter_brand,
        'selected_sort_method': selected_sort_method,
    }

    return render(request, 'products/products.html', context)


def product_details(request, ean_code):
    """ A view to return the product detail page """

    product = get_object_or_404(Product, ean_code=ean_code)
    other_products_same_size = Product.objects.filter(size=product.size).exclude(ean_code=ean_code)

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all().order_by('display_name', )
    sizes = TyreSize.objects.all().order_by('rim_size', 'width',)

    query_search = None
    query_filter_season = None
    query_filter_size = None

    query_filter_brand = None

    if request.GET:
        # Handles free search bar functionality
        if 'q' in request.GET:
            query_search = request.GET['q']
            if not query_search:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
                
            queries = Q(
                name__icontains=query_search) | Q(
                description__icontains=query_search) | Q(
                size__full_size_display__icontains=query_search) | Q(
                size__full_size_code__icontains=query_search) | Q(
                size__full_size_short__icontains=query_search)
            products = products.filter(queries)

        # Handles main filtering functionality
        if 'season' in request.GET:
            query_filter_season = request.GET['season']
            query_filter_size = request.GET['size']

            queries = Q(
                category__name__icontains=query_filter_season) & Q(
                size__full_size_code__icontains=query_filter_size)
            products = products.filter(queries)

        if 'season' and 'brand' in request.GET:
            query_filter_season = request.GET['season']
            query_filter_size = request.GET['size']
            query_filter_brand = request.GET.getlist('brand')
    
            queries = Q(
                category__name__icontains=query_filter_season) & Q(
                size__full_size_code__icontains=query_filter_size)
            query_brand = reduce(operator.or_, (Q(
                manufacturer__name__icontains=each_brand
                ) for each_brand in query_filter_brand))
            products = products.filter(queries).filter(query_brand)

    context = {
        'product': product,
        'other_products_same_size': other_products_same_size,
        'categories': categories,
        'manufacturers': manufacturers,
        'sizes': sizes,
        'search_term': query_search,
        'filter_term_season': query_filter_season,
        'filter_term_size': query_filter_size,
        'filter_term_brand': query_filter_brand,
    }

    return render(request, 'products/product_details.html', context)