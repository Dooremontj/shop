from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    #Gestion produit
    path('product/', login_required(views.ProductListView.as_view()), name='products'),
    path('product/<int:pk>', login_required(views.ProductDetailView.as_view()), name='product-detail'),
    path('product/create/', login_required(views.ProductCreate), name='product-create'),
    path('product/<int:pk>/update/', login_required(views.ProductUpdate), name='product-update'),
    path('product/<int:pk>/delete/', login_required(views.ProductDelete.as_view()), name='product-delete'),
    path('product/<int:pk>/restock/', login_required(views.ProductRestock), name='product-restock'),
    #Gestion Commande
    path('order/', login_required(views.OrderListView.as_view()), name='orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/create/', views.OrderItemCreate.as_view(), name='order-create'),
    path('order/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('order/<int:pk>/delete/', views.OrderDelete.as_view(), name='order-delete'),
    path('order/lastid/', views.OrderLastID, name='order-last-id'),
    #Resident
    path('resident/', views.ResidentListView.as_view(), name='residents'),
    path('resident/create/', views.ResidentCreate, name='resident-create'),
    path('resident/<int:pk>', views.ResidentDetailView.as_view(), name='resident-detail'),
    path('resident/<int:pk>/family', views.ResidentDetailFamilyView, name='resident-detail-family'),
    path('resident/<int:pk>/order', views.ResidentDetailOrderView, name='resident-detail-order'),
    path('resident/<int:pk>/delete/', views.ResidentDelete.as_view(), name='resident-delete'),
    #supplier
    path('supplier/', views.SupplierListView.as_view(), name='suppliers'),
    path('supplier/product/<int:pk>', views.ProductsBySupplierView, name='products-by-supplier'),
    path('supplier/create/', views.SupplierCreate, name='supplier-create'),
    path('supplier/<int:pk>', views.SupplierDetailView.as_view(), name='supplier-detail'),
    path('supplier/<int:pk>/delete/', views.SupplierDelete.as_view(), name='supplier-delete'),
    #other
    path('register', views.register_request, name="register"),
    url(
        r'^product-autocomplete/$',
        views.ProductAutocomplete.as_view(),
        name='product-autocomplete',
    ),
    url(
        r'^resident-autocomplete/$',
        views.ResidentAutocomplete.as_view(),
        name='resident-autocomplete',
    ),
    
]