from django.db.models.signals import user_logged_in
from django.dispatch import receiver
from dashboard.models import CartItem
import pdb
# @receiver(user_logged_in)
# def transfer_cart_on_login(sender, request, user, **kwargs):
#     pdb.set_trace()
#     cart = request.session.get('cart', [])
#     for item_data in cart:
#         quantity = item_data.get('quantity')
#         item_id = item_data.get('item_id')
#         CartItem.objects.create(quantity=quantity, item_id=item_id, user=user)
#     request.user.session.save()
#     request.session.pop('cart', None)