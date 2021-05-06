from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
import datetime
from catalog.mail import *

#Resident 

class Resident(models.Model):
    badge = models.CharField(max_length=100,verbose_name="Badge", blank=True)
    family_group = models.CharField(max_length=2, verbose_name="Composition familiale", blank=True)
    name = models.CharField(max_length=100, verbose_name="Nom", blank=True)
    firstname = models.CharField(max_length=100, verbose_name="Prénom", blank=True)
    room = models.IntegerField(max_length=5, verbose_name="Chambre", blank=True)
    #birthdate = models.DateTimeField(max_length=100, verbose_name="Date de naissance", blank=True)
    age = models.IntegerField(max_length=3,verbose_name="Age", blank=True)
    #datein = models.DateTimeField(max_length=100,verbose_name="Date d'arrivée", blank=True)
    sexe = models.CharField(max_length=1, verbose_name="Sexe", blank=True)
    
    class Meta:
        verbose_name = "Résident"
        ordering = ['badge','family_group','firstname']
        
    def __str__(self):
        """Cette fonction est obligatoirement requise par Django.
           Elle retourne une chaîne de caractère pour identifier l'instance de la classe d'objet."""
        return self.badge+" - "+self.family_group +" ("+self.name+" "+self.firstname+")"


# Fournisseur

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100, verbose_name="Fournisseur")
    supplier_address = models.CharField(max_length=100, verbose_name="Adresse fournisseur", blank=True)
    supplier_mail = models.EmailField(max_length=100, verbose_name="Mail fournisseur", blank=True)
    supplier_tel = models.CharField(max_length=100, verbose_name="Telephone fournisseur", blank=True)
    
    class Meta:
        verbose_name = "Fournisseur"
        ordering = ['supplier_name']
        
    def __str__(self):
        """Cette fonction est obligatoirement requise par Django.
           Elle retourne une chaîne de caractère pour identifier l'instance de la classe d'objet."""
        return self.supplier_name
        
    def get_absolute_url(self):
        """Cette fonction est requise pas Django, lorsque vous souhaitez détailler le contenu d'un objet."""
        return reverse('supplier-detail', args=[str(self.id)])


# Produit

class Product(models.Model):
    prod_name = models.CharField(max_length=100, verbose_name="Nom du produit")
    prod_stock = models.PositiveIntegerField(verbose_name="Quantité en stock", default='0')
    prod_min = models.PositiveIntegerField(verbose_name="Quantité minimal", default='0')
    prod_max = models.PositiveIntegerField(verbose_name="Quantité maximal", default='1')
    prod_ref_in = models.CharField(max_length=100, verbose_name="Référence interne", blank=True, unique=True, error_messages={'unique':"La référence interne existe déja"})
    prod_supplier = models.ForeignKey('Supplier',verbose_name="Fournisseur", on_delete=models.SET_NULL, null=True)
    prod_ref_out = models.CharField(max_length=100, verbose_name="Référence externe", blank=True) 
    prod_date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout", blank=True)
    prod_date_update = models.DateTimeField(auto_now=True, verbose_name="Date de modification", blank=True)
    prod_img = models.ImageField(upload_to='img/product', default='img/product/default_product.png', verbose_name="Image du produit", blank=True)
   
    class Meta:
        verbose_name = "Produit"
        ordering = ['prod_name']

    def __str__(self):
        return self.prod_name
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])








# Commande

class Order (models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(blank=True, max_length=150)
    timestamp = models.DateField(auto_now_add=True)
    order_user = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Commande"
        ordering = ['-date']

    def __str__(self):
        return self.title if self.title else 'New Order'
        
    def get_absolute_url(self):
       """Cette fonction est requise pas Django, lorsque vous souhaitez détailler le contenu d'un objet."""
       return reverse('order-detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('update_order', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('delete_order', kwargs={'pk': self.id})
        
# @receiver(post_save, sender=Order)
# def send_mail(sender, instance, **kwargs):
    # email_new_order(instance)
    
      
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "ligne de commande"
        
    def __str__(self):
        return f'{self.product.prod_name}'

 #   def save(self,  *args, **kwargs):
  #      super().save(*args, **kwargs)
   #     self.order.save()

@receiver(post_delete, sender=OrderItem)
def delete_order_item(sender, instance, **kwargs):
    product = instance.product
    product.prod_stock += instance.qty
    product.save()
    instance.order.save()
    
# @receiver(post_save, sender=OrderItem)
# def save_order_item(sender, instance, **kwargs):
    # product = instance.product
    # product.prod_stock -= instance.qty
    # product.save()
    # if product.prod_stock <= product.prod_min:
        # email_warning_stock(product)
    # instance.order.save()