from functools import reduce
import operator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Manufacturer, TyreSize

from .forms import ProductForm

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
  
            queries = Q(
                category__name__icontains=query_filter_season) & Q(
                size__full_size_code__icontains=query_filter_size)
            query_brand = reduce(operator.or_, (Q(
                manufacturer__name__icontains=each_brand
                ) for each_brand in query_filter_brand))
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


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, You don't have permission to acces this page!")
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_details', args=[product.ean_code]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def update_product(request, ean_code):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, You don't have permission to acces this page!")
        return redirect(reverse('home'))

    product = get_object_or_404(Product, ean_code=ean_code)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_details', args=[product.ean_code]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name} with code {product.ean_code}')

    template = 'products/update_product.html'
    context = {
        'form': form,
        'product': product,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def delete_product(request, ean_code):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, You don't have permission to acces this page!")
        return redirect(reverse('home'))

    product = get_object_or_404(Product, ean_code=ean_code)
    product.delete()
    messages.success(request, 'Product deleted succcessfully!')
    return redirect(reverse('products'))
