from django.shortcuts import render
from catalog.models import Product, Supplier, Order, OrderItem
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.db import transaction
from .forms import *
from dal import autocomplete
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.forms.utils import ErrorList
from catalog.mail import *
from django.http import JsonResponse
from django.core import serializers

def index(request):
	return render(request, 'index.html')

class ProductListView(generic.ListView):
    model = Product
    #paginate_by = 10

class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    
class SupplierListView(LoginRequiredMixin, generic.ListView):
    model = Supplier
     
class SupplierDetailView(LoginRequiredMixin, generic.DetailView):
    model = Supplier

class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    
class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


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
        

class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
           return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(prod_name__istartswith=self.q)

        return qs

def test(request):
    qs = Product.objects.all()
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')
# def email_new_order(request):
    # users = User.objects.filter(groups__name='Shop Members')
    # for user in users:
        # subject = 'Nouvelle commande'
        # message = ' Une nouvelle commande est arrivée'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email,]
        # send_mail( subject, message, email_from, recipient_list )