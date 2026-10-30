from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .choice import bedroom_choices, price_choices, state_choices
from .models import Listing


def index(request):
    listings = Listing.objects.order_by('-list_data').filter(is_Published=True)

    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(
        paged_listings.number,
        on_each_side=2,
        on_ends=1,
    )
    context = {
        'listings': paged_listings,
        'page_range': page_range,
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing_item = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing_item,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_data').filter(is_Published=True)

    # Keywords (searches title, description, address, city, state, zipcode, and garage features)
    if 'keywords' in request.GET:
        keywords = request.GET['keywords'].strip()
        if keywords:
            keyword_query = (
                Q(title__icontains=keywords)
                | Q(description__icontains=keywords)
                | Q(address__icontains=keywords)
                | Q(city__icontains=keywords)
                | Q(state__icontains=keywords)
                | Q(zipcode__icontains=keywords)
            )
            # If search term contains garage or car keywords, match garage > 0 as well
            if any(term in keywords.lower() for term in ('garage', 'parking', 'car')):
                keyword_query |= Q(garage__gt=0)
            queryset_list = queryset_list.filter(keyword_query)

    # City (case-insensitive)
    if 'city' in request.GET:
        city = request.GET['city'].strip()
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state'].strip()
        if state and state.lower() != 'state (all)':
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms'].strip()
        if bedrooms and bedrooms.lower() != 'bedrooms (any)':
            try:
                queryset_list = queryset_list.filter(bedrooms__lte=int(bedrooms))
            except ValueError:
                pass

    # Price (maximum price ceiling)
    if 'price' in request.GET:
        price = request.GET['price'].strip()
        if price and price.lower() != 'max price (all)':
            try:
                queryset_list = queryset_list.filter(price__lte=int(price))
            except ValueError:
                pass

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }
    return render(request, 'listings/search.html', context)
