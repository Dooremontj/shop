from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Supplier, Order, OrderItem, Resident
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


def index(request):
	return render(request, 'index.html')
    
    
################################################################################################
#products
################################################################################################

class ProductListView(generic.ListView):
    model = Product
    #paginate_by = 10
    
class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    

    
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
    if form.is_valid():
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
        can_save = True
        d = dict()
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
                    if prod.id in d :
                        qty = d.get(prod.id)
                        qty += f.cleaned_data['qty']
                        d[prod.id] = qty
                    else:
                        qty = f.cleaned_data['qty']
                        d[prod.id] = qty
        for key in d :
            product = Product.objects.get(pk=key)
            if product.prod_stock < d.get(key):
                can_save = False
                form.add_error(None,'Problème de quantitée pour le produit :'+ product.prod_name + ' Quantité restante : '+ str(product.prod_stock))
                form.add_error(None,'Quantité restante : '+ str(product.prod_stock))
                form.add_error(None,'Quantité demandée : '+ str(d.get(key)))
                break
        if can_save and orderlist.is_valid():
            response = super().form_valid(form)
            orderlist.instance = self.object
            orderlist.save()
            for key in d :
                product = Product.objects.get(pk=key)
                product.prod_stock = product.prod_stock-d.get(key)
                product.save()
                if product.prod_stock <= product.prod_min:
                    email_warning_stock(product)
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