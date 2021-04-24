from dal import autocomplete
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

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
        if Product.objects.filter(prod_supplier=self.cleaned_data['prod_supplier'], prod_ref_out = self.cleaned_data['prod_ref_out']).count() ==1 :
            errors['prod_ref_out'] = _('La référence externe existe déja pour ce fournisseur')
        if Product.objects.filter(prod_ref_in=self.cleaned_data['prod_ref_in']).count() == 1:
            errors['prod_ref_in'] = _('La référence interne existe déja')
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
        prod = self.cleaned_data['product']
        product_selected = Product.objects.get(pk=prod.id)
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
    
    class Meta:
        model = Order
        fields = '__all__'
        
class ResidentForm(forms.ModelForm):
    
    class Meta:
        model = Resident
        fields = '__all__'
    
    
    # def clean(self):
        # errors ={}
        # errors['title'] = _('Stock du produit insuffisant - stock restant :' )
        # if errors:
            # raise ValidationError(errors)