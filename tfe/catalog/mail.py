from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User, Group

def email_new_order(order):
    users = User.objects.filter(groups__name='Shop Members')
    for user in users:
        subject = 'Nouvelle commande - ' + order.title
        message = ' Une nouvelle commande a été fait par ' + order.order_user.username
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,]
        send_mail( subject, message, email_from, recipient_list )
        
def email_warning_stock(product):
    users = User.objects.filter(groups__name='Shop Members')
    for user in users:
        subject = 'Alerte Stock - ' + product.prod_name
        message = ' Le produit : ' + product.prod_name + ' est bientôt en rupture de stock ! (quantité restante : ' + str(product.prod_stock) + ')' 
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,]
        send_mail( subject, message, email_from, recipient_list )