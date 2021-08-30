from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Supplier, Order, OrderItem, Basket, BasketResident, Resident, FedOrder, FedOrderItem, LimitFamily
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .forms import *
from dal import autocomplete
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.forms.utils import ErrorList
from catalog.mail import *
from django.core import serializers
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import permission_required

def index(request):
	return render(request, 'index.html')
    
    
################################################################################################
#products
################################################################################################

class ProductListView(generic.ListView):
    model = Product
    
def ProductListResidentView(request):
    user_basket = Resident.objects.all()
    products = Product.objects.filter(prod_main_category='RESIDENT')
    return render(request,'catalog/product_list_resident.html', {'product_list':products,'user_basket' : user_basket})
    
class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    
def ProductListShop(request):
    products = Product.objects.filter(prod_main_category='PERSONNEL')
    return render(request,'catalog/product_list_shop.html', {'product_list':products})


def ProductCreate(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('products') )
    else:
        form = ProductCreateForm()
    return render(request, 'catalog/product_create_form.html', {
            'form': form,
    })
    
def ProductUpdate(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    form = ProductUpdateForm(request.POST or None, instance=instance)
    can_save = False
    product_list = Product.objects.exclude(pk=instance.pk)
    oldObject = get_object_or_404(Product, pk=pk)
    if form.is_valid():
        if oldObject.prod_ref_in != form.cleaned_data['prod_ref_in']:
            if product_list.filter(prod_ref_in=form.cleaned_data.get('prod_ref_in')).exists():
                form.add_error('prod_ref_in','La référence interne existe déja')
                return render(request, 'catalog/product_form.html', {'form': form}) 
        if oldObject.prod_ref_out != form.cleaned_data['prod_ref_out'] or oldObject.prod_supplier != form.cleaned_data['prod_supplier']:
            if product_list.filter(prod_supplier=form.cleaned_data.get('prod_supplier'),prod_ref_out=form.cleaned_data.get('prod_ref_out')).exists():
                form.add_error('prod_ref_out','La référence externe existe déja')
                return render(request, 'catalog/product_form.html', {'form': form}) 
        form.save()
        return HttpResponseRedirect(reverse('products') )
    return render(request, 'catalog/product_form.html', {'form': form}) 
    

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('products')

def ProductsBySupplierView(request, pk):
    model = Product
    products = Product.objects.filter(prod_supplier=pk)
    return render(request,'catalog/products_by_supplier.html', {'products': products})

class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
           return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(prod_name__istartswith=self.q)

        return qs 
        
def ProductRestock(request, pk):
    instance=get_object_or_404(Product, pk = pk)

    if request.method == 'POST':

        form = RestockProductForm(request.POST)

        if form.is_valid():
            instance.prod_stock += form.cleaned_data['qty_in']
            instance.save()
            return HttpResponseRedirect(reverse('products') )

    else:
        min = 1
        form = RestockProductForm(initial={'qty_in': min,})

    return render(request, 'catalog/restock_product_form.html', {'form': form, 'product':instance})
    
    
################################################################################################
#Basket
################################################################################################

def AddBasket(request):
    if request.method == 'POST':
        productselected = get_object_or_404(Product, pk=request.POST.get('product'))
        if Basket.objects.filter(product=productselected, user_basket=request.user).exists():
            instancebasket = get_object_or_404(Basket, product=productselected, user_basket=request.user)
            instancebasket.qty += int(request.POST.get('qty'))
            instancebasket.save()
        else:
            instance = Basket(product=productselected , qty=request.POST.get('qty') , user_basket=request.user)
            instance.save()
    return HttpResponseRedirect(reverse('product-shop') )
    
def AddBasketResident(request,pk):
    if request.method == 'POST':
        productselected = get_object_or_404(Product, pk=pk)
        residentselected =  get_object_or_404(Resident, pk=request.POST.get('user_basket'))
        if BasketResident.objects.filter(product=productselected, user_basket=residentselected).exists():
            instancebasket = get_object_or_404(BasketResident, product=productselected, user_basket=residentselected)
            instancebasket.qty += int(request.POST.get('qty'))
            instancebasket.save()
        else:
            instance = BasketResident(product=productselected , qty=request.POST.get('qty') , user_basket=residentselected)
            instance.save()
    return HttpResponseRedirect(reverse('product-shop') )
    
def BasketListView(request):
    product_list = Basket.objects.filter(user_basket=request.user)
    return render(request,'catalog/basket.html', {'product_list':product_list})
    
def BasketResidentListView(request,pk):
    product_list = BasketResident.objects.filter(user_basket=pk)
    points = 0
    for p in product_list :
        points += p.product.prod_limit
    instance = get_object_or_404(Resident, pk=pk)
    family = Resident.objects.filter(badge=instance.badge)
    familynumber = family.count()
    user_points = get_object_or_404(LimitFamily, compo_family=str(familynumber)).point_by_week
    return render(request,'catalog/basket_resident_detail.html', {'product_list':product_list, 'points':points, 'user_points':user_points})
    
def BasketDelete(request):
    product_list = Basket.objects.filter(user_basket=request.user)
    for p in product_list :
        p.delete()
    return HttpResponseRedirect(reverse('basket') )
    
def BasketConvert(request):
    product = Product.objects.all()
    order_list = Basket.objects.filter(user_basket=request.user)
    can_save = True
    for p in order_list :
        product = get_object_or_404(Product, pk=p.product.pk)
        if p.qty >= product.prod_stock:
            p.error = "Stock insuffisant - Stock restant :"+ str(product.prod_stock)
            p.save()
            can_save = False
    if can_save:
        id = FedOrder.objects.latest('id')
        title = "AMC_Fed_"+datetime.datetime.now().strftime ("%d%m%Y")+"_"+str((id.id+1))
        instance_order = FedOrder(order_user=request.user,title=title)
        instance_order.save()
        for p in order_list :
            instance_item = FedOrderItem(product=p.product,order=instance_order,qty=p.qty)
            instance_item.save()
            p.delete()
    return HttpResponseRedirect(reverse('basket') )

def ProductAddOne(request, pk):
    instance=get_object_or_404(Basket, pk = pk)

    if request.method == 'POST':
            instance.qty += 1
            instance.save()
    return HttpResponseRedirect(reverse('basket') )

    
def ProductRemoveOne(request, pk):
    instance=get_object_or_404(Basket, pk = pk)

    if request.method == 'POST':
        if instance.qty - 1 > 0 :
            instance.qty -= 1
            instance.save()
        elif instance.qty - 1 == 0:
            instance.delete()
    return HttpResponseRedirect(reverse('basket') )
    
################################################################################################
#Commande Personnel
################################################################################################

class FedOrderListView(generic.ListView):
    model = FedOrder

class FedOrderDelete(DeleteView):
    model = FedOrder
    success_url = reverse_lazy('fed-orders')
    
def MyFedOrderListView(request):
    fedorder_list = FedOrder.objects.filter(order_user=request.user)
    return render(request, 'catalog/fedorder_list.html', {
            'fedorder_list': fedorder_list,
    })

class FedOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = FedOrder

@permission_required('catalog.can_close_order')
def FedOrderClose(request, pk):
    instance = get_object_or_404(FedOrder, pk=pk)
    instance.status = "CLOSED"
    instance.save()
    fedorderitem = FedOrderItem.objects.filter(order = instance)
    for f in fedorderitem:
        instance_product = get_object_or_404(Product, pk = f.product.pk)
        instance_product.prod_stock = instance_product.prod_stock-f.qty
        instance_product.save()
    fedorder_list = FedOrder.objects.all()
    return HttpResponseRedirect(reverse('fed-orders'))

def FedOrderUpdateView(request, pk):
    instance = get_object_or_404(FedOrder, pk=pk)
    return render(request, 'catalog/fedorder_update.html', {
            'order': instance,
    })
    
def FedOrderItemUpdateView(request,pk):
    instance = get_object_or_404(FedOrderItem, pk=pk)
    instance.qty = request.POST.get('qty')
    instance.save()
    return render(request, 'catalog/fedorder_update.html', {
            'fedorderitem': instance,
    })
   
################################################################################################
#suppliers
################################################################################################

class SupplierListView(LoginRequiredMixin, generic.ListView):
    model = Supplier
     
class SupplierDetailView(LoginRequiredMixin, generic.DetailView):
    model = Supplier

def SupplierCreate(request):
    if request.method == 'POST':
        form = SupplierCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('suppliers') )
    else:
        form = SupplierCreateForm()
    return render(request, 'catalog/supplier_create_form.html', {
            'form': form,
    })

class SupplierDelete(DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers')
    
################################################################################################    
#residents
################################################################################################   

class ResidentListView(LoginRequiredMixin, generic.ListView):
    model = Resident
    
class ResidentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Resident

def ResidentDetailFamilyView(request, pk):
    model = Resident
    instance = get_object_or_404(Resident, pk=pk)
    family = Resident.objects.filter(badge=instance.badge).order_by('-age')
    familynumber = family.count()
    child = 0
    for f in family:
        if f.age < 12:
            child += 1
    return render(request,'catalog/family_detail.html', {'child':child, 'resident': instance, 'family' : family, 'familynumber':familynumber})
    
def ResidentDetailOrderView(request, pk):
    model = Resident
    instance = get_object_or_404(Resident, pk=pk)
    family = Resident.objects.filter(badge=instance.badge)
    pklist = []
    for f in family:
        pklist.append(f.id)
    order_list = Order.objects.filter(order_user__in=pklist)
    return render(request,'catalog/family_detail_order.html', {'order_list':order_list})

class ResidentDelete(DeleteView):
    model = Resident
    success_url = reverse_lazy('residents')
    
def ResidentCreate(request):
    if request.method == 'POST':
        form = ResidentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('resident') )
    else:
        form = ResidentCreateForm()
    return render(request, 'catalog/resident_create_form.html', {
            'form': form,
    })
################################################################################################    
#Orders
################################################################################################   
    

    
class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    
class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')
    
class OrderItemCreate(CreateView):
    form_class = OrderForm
    template_name = 'catalog/order_form.html'
    # model = Order
    # fields = '__all__'
    success_url = reverse_lazy('orders')
    
    def get_context_data(self, **kwargs):
        data = super(OrderItemCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderlist'] = OrderItemFormSet(self.request.POST)
            
        else:
            data['orderlist'] = OrderItemFormSet()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        orderlist = context['orderlist']
        # residentselected = context['form'].cleaned_data.get('order_user')      
        # resident = get_object_or_404(Resident, pk=residentselected.pk)
        # family = Resident.objects.filter(badge=resident.badge).order_by('-age')
        # familynumber = family.count()
        # limit = get_object_or_404(LimitFamily, compo_family=str(familynumber))
        can_save = True
        d = dict()
        point = 0
        for f in orderlist:
            if f.is_valid():
                if f.cleaned_data.get('product') is None :
                    form.add_error(None,'Aucun produit sélectionner')
                    can_save = False
                if f.cleaned_data.get('qty') is None :
                    form.add_error(None,'La quantité ne peut pas être nulle')
                    can_save = False
                else : 
                    prod = f.cleaned_data['product']
                    point += prod.prod_limit
                    if prod.id in d :
                        qty = d.get(prod.id)
                        qty += f.cleaned_data['qty']
                        d[prod.id] = qty
                    else:
                        qty = f.cleaned_data['qty']
                        d[prod.id] = qty

        form.data = form.data.copy()
        form.data['points'] = 50
        orderlist.data = orderlist.data.copy()
        orderlist.data['points'] = 50
        # if point > limit.point_by_week : 
            # form.add_error(None,'Limite de point dépasse de : '+str(point))
            # can_save = False
            # return super().form_invalid(form)
        if can_save and orderlist.is_valid():
            
            response = super().form_valid(form)
            orderlist.instance = self.object
            orderlist.save()
            for key in d :
                product = Product.objects.get(pk=key)
                product.prod_stock = product.prod_stock-d.get(key)
                product.save()
                # if product.prod_stock <= product.prod_min:
                    # email_warning_stock(product)
            return response
        else:
            return super().form_invalid(form)
        return super(OrderItemCreate, self).form_valid(form)
 
        
class OrderUpdate(UpdateView):
    model = Order
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderlist'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['orderlist'] = OrderItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderlist = context['orderlist']
        if orderlist.is_valid():
            response = super().form_valid(form)
            orderlist.instance = self.object
            orderlist.save()
            return response
        else:
            return super().form_invalid(form)
        return super(OrderUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('order-detail', kwargs={'pk': self.object.pk})
        
def OrderLastID(request):
    model = Order
    instance = Order.objects.latest('id')
    return HttpResponse(instance.id+1)


    
    
    

        
class ResidentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
           return Resident.objects.none()

        qs = Resident.objects.all()

        if self.q:
            qs = qs.filter(badge__istartswith=self.q)

        return qs

    
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return HttpResponseRedirect(reverse('products'))
		form.add_error(None,request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"form":form})
   
# def email_new_order(request):
    # users = User.objects.filter(groups__name='Shop Members')
    # for user in users:
        # subject = 'Nouvelle commande'
        # message = ' Une nouvelle commande est arrivée'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email,]
        # send_mail( subject, message, email_from, recipient_list )