from django.urls import path

from management import views as management_views

urlpatterns = [
  path('attendance_query/', management_views.attendance_query,
       name='attendance_query'),
  path('customer-record-query/', management_views.customer_record_query,
       name='customer_record_query'),
  path('delete/<int:record_id>/', management_views.delete_customer_record,
       name='delete_customer_record'),

  path('create/', management_views.create_expense, name='create_expense'),
  path('query_expense_list/', management_views.expense_list,
       name='expense_list'),
  path('receipt/<int:pk>/', management_views.view_receipt, name='view_receipt'),
]
