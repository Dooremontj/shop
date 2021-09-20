from dal import autocomplete
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><br><img class="img-fluid img-thumbnail" src="{value.url}"/>')
        return f'{input_html}{img_html}'

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ='__all__'
        
    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        errors={}
        if self.cleaned_data['prod_min'] >= self.cleaned_data['prod_max']:
            errors['prod_min']= _('La quantité minimale ne peut pas être supérieur ou égale à la quantité maximale')
        if self.cleaned_data['prod_max'] is None:
            errors['prod_max'] = _('La quantité maximale ne peut pas être nulle')
        if errors:
            raise ValidationError(errors)
        return self.cleaned_data
            
class ProductCreateForm(forms.ModelForm):
            
    class Meta:
        model = Product
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
    def clean(self):
        errors={}
        if self.cleaned_data['prod_min'] >= self.cleaned_data['prod_max']:
            errors['prod_min']= _('La quantité minimale ne peut pas être supérieur ou égale à la quantité maximale')
        if self.cleaned_data['prod_max'] is None:
            errors['prod_max'] = _('La quantité maximale ne peut pas être nulle')
        if self.cleaned_data['prod_ref_out'] != "" :
            if Product.objects.filter(prod_supplier=self.cleaned_data['prod_supplier'], prod_ref_out = self.cleaned_data['prod_ref_out']).count() ==1 :
                errors['prod_ref_out'] = _('La référence externe existe déja pour ce fournisseur')
        if self.cleaned_data['prod_ref_in'] != "":
            if Product.objects.filter(prod_ref_in=self.cleaned_data['prod_ref_in']).count() == 1:
                errors['prod_ref_in'] = _('La référence interne existe déja')
        if errors:
            raise ValidationError(errors)
        return self.cleaned_data

class SupplierCreateForm(forms.ModelForm):
            
    class Meta:
        model = Supplier
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(SupplierCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
    # def clean(self):
        # errors={}
        # if Supplier.objects.filter(supplier_name = self.cleaned_data['supplier_name']).count() == 1:
            # errors['supplier_name']= _('Le fournisseur existe déja')
        # if Supplier.objects.filter(supplier_mail = self.cleaned_data['supplier_mail']).count() == 1:
            # errors['supplier_mail']= _('L adresse mail existe déja')
        # if Supplier.objects.filter(supplier_tel = self.cleaned_data['supplier_tel']).count() == 1:
            # errors['supplier_tel']= _('Le numéro de téléphone existe déja')
        # if errors:
            # raise ValidationError(errors)
        # return self.cleaned_data
        
class ResidentCreateForm(forms.ModelForm):
            
    class Meta:
        model = Resident
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(ResidentCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
    def clean(self):
        if errors:
            raise ValidationError(errors)
        return self.cleaned_data

class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='product-autocomplete')
    )
    
    
    class Meta:
        model = OrderItem
        fields = ('__all__')
    
    def clean(self):
        errors={}
        if self.cleaned_data.get('product') is None :
            errors['product'] = _('pas de produits sélectionner')
        else :
            prod = self.cleaned_data['product']
            product_selected = Product.objects.get(pk=prod.id)
            if self.cleaned_data.get('qty') is None or self.cleaned_data.get('qty') == 0 :
                errors['qty'] = _('pas de quantité')
            else : 
                if product_selected.prod_stock-self.cleaned_data['qty'] < 0:
                     errors['qty'] = _('Stock du produit insuffisant - stock restant :'+ str(product_selected.prod_stock) )
        if errors:
            raise ValidationError(errors)
        return self.cleaned_data

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=1, can_delete=True
    )

class OrderForm(forms.ModelForm):
    order_user = forms.ModelChoiceField(
        queryset=Resident.objects.all(),
        widget=autocomplete.ModelSelect2(url='resident-autocomplete')
    )
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(OrderForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        errors={}
        residentselected = self.cleaned_data.get('order_user')      
        resident = Resident.objects.get(pk=residentselected.id)
        family = Resident.objects.filter(badge=resident.badge).order_by('-age')
        familynumber = family.count()
        limit = LimitFamily.objects.get(compo_family=str(familynumber))
        if self.cleaned_data.get('points') > limit.point_by_week :
            errors['points'] = _(str(self.cleaned_data.get('points')))
        if errors:
            raise ValidationError(errors)
        return self.cleaned_data

            
class ResidentForm(forms.ModelForm):
    
    class Meta:
        model = Resident
        fields = '__all__'

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(NewUserForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'    
        

            
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class RestockProductForm(forms.Form):
    qty_in = forms.IntegerField(min_value=1, help_text="Entrez le stock réceptionné")

    
    