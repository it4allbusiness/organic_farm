from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView
#from .views import stripe_payment

urlpatterns = [
    path('', views.general_page, name='general-page'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),

    path('signup', views.signup, name='signup'),

    path('admin-signup', views.admin_signup, name='admin-signup'),
    path('admin-page', views.admin_page, name='admin-page'),
    path('admin-assistant-detail/<int:pk>/', views.admin_assistant_detail, name='admin-assistant-detail'),
    path('admin-approve-assistant/<int:pk>/', views.admin_approve_assistant, name='admin-approve-assistant'),
    path('admin-employee', views.admin_employee, name='admin-employee'),
    path('admin-employee-detail/<int:pk>/', views.admin_employee_detail, name='admin-employee-detail'),
    path('admin-approve-employee/<int:pk>/', views.admin_approve_employee, name='admin-approve-employee'),

    path('employee-signup', views.employee_signup, name='employee-signup'),
    path('customer-signup', views.customer_signup, name='customer-signup'),
    path('customer-page', views.customer_page, name='customer-page'),


    path('login', LoginView.as_view(template_name='business/login.html'),name='login'),
    path('logout', LogoutView.as_view(template_name='business/logout.html'),name='logout'),

    path('after-login', views.after_login, name='after-login'),
    path('assistant-page', views.assistant_page, name='assistant-page'),

    path('assistant-employee', views.assistant_employee, name='assistant-employee'),
    path('assistant-employee-detail/<int:pk>/', views.assistant_employee_detail, name='assistant-employee-detail'),
    path('assistant-approve-employee/<int:pk>/', views.assistant_approve_employee, name='assistant-approve-employee'),
    path('assistant-delete-employee/<int:pk>/', views.assistant_delete_employee, name='assistant-delete-employee'),
    path('assistant-update-employee/<int:pk>/', views.assistant_update_employee, name='assistant-update-employee'),

    path('assistant-category', views.assistant_category, name='assistant-category'),
    path('assistant-add-category', views.assistant_add_category, name='assistant-add-category'),
    path('assistant-delete-category/<int:pk>/', views.assistant_delete_category, name='assistant-delete-category'),

    path('assistant-product', views.assistant_product, name='assistant-product'),
    path('assistant-add-product', views.assistant_add_product, name='assistant-add-product'),
    path('assistant-update-product/<int:pk>/', views.assistant_update_product, name='assistant-update-product'),
    path('assistant-delete-product/<int:pk>/', views.assistant_delete_product, name='assistant-delete-product'),

    path('associate-page', views.associate_page, name='associate-page'),
    path('employee-page', views.employee_page, name='employee-page'),

    path('add-product-to-cart/<int:pk>',views.add_product_to_cart, name='add-product-to-cart'),
    path('order-summary',views.order_summary, name='order-summary'),
    path('order-checkout',views.order_checkout, name='order-checkout'),
    path('my-order',views.my_order, name='my-order'),
    
    #path('stripe-payment/', stripe_payment.as_view(), name='stripe-payment'),
    path('contact-us', views.contactus_view,name='contact-us'),
   
    path('assistant-update-order-status/<int:pk>/', views.assistant_update_order_status, name='assistant-update-order-status'),
    path('assistant-view-order', views.assistant_view_order, name='assistant-view-order'),
    
]