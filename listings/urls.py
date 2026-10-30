from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('',views.index,name='listings'),
    path(
        'listings.html',
        RedirectView.as_view(url='/listings/', permanent=False),
    ),
    path('<int:listing_id>',views.listing,name='listing'),
    path('search',views.search,name='search'),
]