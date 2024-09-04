from django.urls import path
from customer import views as customer_views

urlpatterns = [
  path('', customer_views.customer_search, name='customer_search'),
  path('add/', customer_views.customer_add, name='customer_add'),
  path('maintain/<str:customer_id>/', customer_views.customer_maintain,
       name='customer_maintain'),
  path('add-record/', customer_views.customer_record_create_view,
       name='add_customer_record'),
  path('search/', customer_views.search_by_license_plate,
       name='search_by_license_plate'),
  path('records/', customer_views.customer_recordlist_view,
       name='customer_record_list'),
]
