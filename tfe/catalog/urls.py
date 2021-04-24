from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.ProductListView.as_view(), name='products'),
    path('supplier/', views.SupplierListView.as_view(), name='suppliers'),
    path('order/', views.OrderListView.as_view(), name='orders'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('supplier/<int:pk>', views.SupplierDetailView.as_view(), name='supplier-detail'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    #Gestion produit
    path('product/create/', views.ProductCreate, name='product-create'),
    path('product/<int:pk>/update/', views.ProductUpdate, name='product-update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product-delete'),
    #Gestion Commande
    path('order/create/', views.OrderItemCreate.as_view(), name='order-create'),
    path('order/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('order/<int:pk>/delete/', views.OrderDelete.as_view(), name='order-delete'),
    path('test', views.test, name='test'),
    #path('product-autocomplete/', views.ProductAutocomplete.as_view(), name='product-autocomplete'),
    url(
        r'^product-autocomplete/$',
        views.ProductAutocomplete.as_view(),
        name='product-autocomplete',
    ),
    
]