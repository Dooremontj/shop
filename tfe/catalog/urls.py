from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    #Gestion produit
    path('print/<int:pk>', login_required(views.PrintOrder), name='print'),
    path('consommation/', login_required(views.ConsommationView), name='consommation'),
    path('product/', login_required(views.ProductListView.as_view()), name='products'),
    path('product/warning/', login_required(views.ProductListWarningView), name='products-warning'),
    path('product/out/', login_required(views.ProductListOutView), name='products-out'),
    path('product/<int:pk>', login_required(views.ProductDetailView.as_view()), name='product-detail'),
    path('product/create/', login_required(views.ProductCreate), name='product-create'),
    path('product/<int:pk>/update/', login_required(views.ProductUpdate), name='product-update'),
    path('product/<int:pk>/delete/', login_required(views.ProductDelete.as_view()), name='product-delete'),
    path('product/<int:pk>/restock/', login_required(views.ProductRestock), name='product-restock'),
    path('product/shop/', login_required(views.ProductListShop), name='product-shop'),
    #Gestion panier
    path('product/addtobasket/<int:pk>', login_required(views.AddBasket), name='add-basket'),
    path('product/addtobasketresident/<int:pk>', login_required(views.AddBasketResident), name='add-basket-resident'),
    path('product/<int:pk>/addone/', login_required(views.ProductAddOne), name='product-add-one'),
    path('product/<int:pk>/remove/', login_required(views.ProductRemoveOne), name='product-remove-one'),
    path('basketresident/<int:pk>/add/', login_required(views.BasketResidentAddOne), name='basketresident-add-one'),
    path('basketresident/<int:pk>/remove/', login_required(views.BasketResidentRemoveOne), name='basketresident-remove-one'),
    path('basket/', login_required(views.BasketListView), name='basket'),
    path('basketresident/<int:pk>', login_required(views.BasketResidentListView), name='basket-resident-detail'),
    path('basket/delete', login_required(views.BasketDelete), name='basket-delete'),
    path('basketresident/<int:pk>/delete', login_required(views.BasketResidentDelete), name='basketresident-delete'),
    path('basket/convert', login_required(views.BasketConvert), name='basket-convert'),
    path('basketresident/<int:pk>/convert', login_required(views.BasketResidentConvert), name='basketresident-convert'),
    #Gestion commande du personnel
    path('fed-orders/', login_required(views.FedOrderListView), name='fed-orders'),
    path('fed-order/<int:pk>/delete/', login_required(views.FedOrderDelete.as_view()), name='fed-order-delete'),
    path('fed-order/<int:pk>', login_required(views.FedOrderDetailView.as_view()), name='fed-order-detail'),
    path('my-fed-orders/', login_required(views.MyFedOrderListView), name='my-fed-orders'),
    path('my-fed-orders/<int:pk>/close', login_required(views.FedOrderClose), name='fed-order-closed'),
    # path('my-fed-orders/<int:pk>/partiel', login_required(views.FedOrderPartiel), name='fed-order-partiel'),
    path('my-fed-orders/<int:pk>/update', login_required(views.FedOrderUpdateView), name='fed-order-update'),
    path('fed-orderitem/<int:pk>/update/', login_required(views.FedOrderItemUpdateView), name='fed-orderitem-update'),
    #Gestion Commande
    # path('order/', login_required(views.OrderListView.as_view()), name='orders'),
    # path('product/addtobasketresident/<int:pk>', login_required(views.AddBasketResident), name='add-basket-resident'),
    path('order/', login_required(views.ProductListResidentView), name='orders'),
    path('order/<int:pk>', login_required(views.OrderDetailView.as_view()), name='order-detail'),
    path('order/create/', login_required(views.OrderItemCreate.as_view()), name='order-create'),
    path('order/<int:pk>/update/', login_required(views.OrderUpdate.as_view()), name='order-update'),
    path('order/<int:pk>/delete/', login_required(views.OrderDelete.as_view()), name='order-delete'),
    path('order/lastid/', login_required(views.OrderLastID), name='order-last-id'),
    #Resident
    path('resident/', login_required(views.ResidentListView.as_view()), name='residents'),
    path('resident/create/', login_required(views.ResidentCreate), name='resident-create'),
    path('resident/<int:pk>', login_required(views.ResidentDetailView.as_view()), name='resident-detail'),
    path('resident/<int:pk>/family', login_required(views.ResidentDetailFamilyView), name='resident-detail-family'),
    path('resident/<int:pk>/order', login_required(views.ResidentDetailOrderView), name='resident-detail-order'),
    path('resident/<int:pk>/delete/', login_required(views.ResidentDelete.as_view()), name='resident-delete'),
    #supplier
    path('supplier/', login_required(views.SupplierListView.as_view()), name='suppliers'),
    path('supplier/product/<int:pk>', login_required(views.ProductsBySupplierView), name='products-by-supplier'),
    path('supplier/create/', login_required(views.SupplierCreate), name='supplier-create'),
    path('supplier/<int:pk>', login_required(views.SupplierDetailView.as_view()), name='supplier-detail'),
    path('supplier/<int:pk>/delete/', login_required(views.SupplierDelete.as_view()), name='supplier-delete'),
    #other
    path('register', views.register_request, name="register"),
    url(
        r'^product-autocomplete/$',
        login_required(views.ProductAutocomplete.as_view()),
        name='product-autocomplete',
    ),
    url(
        r'^resident-autocomplete/$',
        login_required(views.ResidentAutocomplete.as_view()),
        name='resident-autocomplete',
    ),
    
]