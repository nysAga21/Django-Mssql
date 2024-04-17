# myapp/urls.py

from django.urls import path
from . import views
from .views import new_query,get_customer_details,get_ciff,makeAccounts,display

app_name="ok"

urlpatterns = [
    path('employees/', views.employee_list, name='employee_list'),
    path('query/', new_query, name='query'),
    path('get_ciffs/<str:ciff>', get_ciff, name='ciff'),
    path('makeAccounts/', makeAccounts, name='makeAccounts'),
    path('display/', display, name='new'),
    path('get_customer_details/<str:account_number>/', get_customer_details, name='get_customer_details'),
    path('link-to-gra/', views.link_to_gra, name='link_to_gra'),
]
