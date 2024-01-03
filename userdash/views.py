from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from dashboard.models import Category, Item, CartItem, Order, Resturant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count, F


class UserHomeView(View):
    def get(self, request):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.filter(retired=False)

        return render(
            request,
            "userdash/userhome.html",
            {"resturants": resturants, "categories": categories, "items": items},
        )


class CategoryItemsView(View):
    def get(self, request, cg_id):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.filter(category__id=cg_id)
        if request.user.is_authenticated and request.user.is_staff:
            return render(
                request,
                "dashboard/dashboard.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )
        else:
            return render(
                request,
                "userdash/userhome.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )


class ResturantItemsView(View):
    def get(self, request, rest_id):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.filter(resturant__id=rest_id)
        if request.user.is_authenticated and request.user.is_staff:
            return render(
                request,
                "dashboard/dashboard.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )
        else:
            return render(
                request,
                "userdash/userhome.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )


class ItemDetail(DetailView):
    model = Item
    template_name = "userdash/item_detail.html"
    context_object_name = "item"


class PopularItemView(View):
    def get(self, request):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        item_dict = (
            CartItem.objects.values("item__title")
            .annotate(max=Count("item__title"))
            .order_by("-max")
            .first()
        )
        try:
            items = Item.objects.filter(title=item_dict["item__title"])
        except:
            messages.warning(request, "There is no order placed by any user yet")
        finally:
            return render(
                request,
                "userdash/userhome.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )


class AddToCart(View):
    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except:
            messages.warning(request, "This Item is not existing")
            return redirect("userhome")
        resturant = item.resturant
        if request.user.is_authenticated and not request.user.is_staff:
            try:
                cartitem = CartItem.objects.get(
                    item=item, order=None, user=request.user
                )
                cartitem.quantity += 1
                cartitem.save()
                messages.success(
                    request, "Item already in your cart! quantity is increased by 1"
                )
            except:
                cartitems = CartItem.objects.filter(
                    order=None, user=request.user
                ).first()
                if cartitems and cartitems.item.resturant.id != resturant.id:
                    messages.warning(
                        request, "You can only add items from one restaurant at a time."
                    )
                    return redirect("userhome")
                CartItem.objects.create(
                    item=item,
                    quantity=1,
                    order=None,
                    user=request.user,
                )
                messages.success(request, "Item was added to cart successfuly")
            finally:
                return redirect("userhome")
        else:
            current_resturant_id = request.session.get("resturant_id")
            if current_resturant_id and current_resturant_id != resturant.id:
                messages.warning(
                    request, "You can only add items from one restaurant at a time."
                )
                return redirect("userhome")
            cart = request.session.get("cart", [])

            for cart_item in cart:
                if cart_item["id"] == item.id:
                    cart_item["quantity"] += 1
                    cart_item["stprice"] = cart_item["quantity"] * cart_item["price"]
                    request.session.save()
                    messages.success(
                        request, "Item already in your cart! quantity is increased by 1"
                    )
                    return redirect("userhome")
            cart.append(
                {
                    "id": item.id,
                    "name": item.title,
                    "quantity": 1,
                    "price": float(item.price),
                    "stprice": float(item.price),
                }
            )
            request.session["cart"] = cart
            request.session["resturant_id"] = resturant.id
            request.session.save()
            messages.success(request, "Item was added to cart successfuly")
            return redirect("userhome")


class MyCart(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            cart = CartItem.objects.filter(user=request.user, order=None).annotate(
                stprice=F("quantity") * F("item__price")
            )
            total_items = sum(item.quantity for item in cart)
            total_price = sum(item.stprice for item in cart)
        else:
            cart = request.session.get("cart", [])
            total_items = sum(item["quantity"] for item in cart)
            total_price = sum(item["stprice"] for item in cart)
        return render(
            request,
            "userdash/mycart.html",
            {"cart": cart, "total_items": total_items, "total_price": total_price},
        )


class ClearCart(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            items = CartItem.objects.filter(user=request.user, order=None)
            items.delete()
        else:
            request.session.pop("cart", None)
            request.session.pop("resturant_id", None)
        return redirect("userhome")


class RemoveFromCart(View):
    def get(self, request, item_id):
        if request.user.is_authenticated and not request.user.is_staff:
            item = CartItem.objects.filter(id=item_id, order_id=None)
            item.delete()
        else:
            cart = request.session.get("cart", [])
            index_to_remove = None
            for i, item in enumerate(cart):
                if item["id"] == item_id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                cart.pop(index_to_remove)
                request.session["cart"] = cart
                request.session.save()
        return redirect("mycart")


class CheckOutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request):
        cartitems = CartItem.objects.filter(user=request.user, order=None)
        if cartitems.exists():
            order = Order.objects.create(user=request.user)
            cartitems.update(order=order)
            messages.success(request, "Your Order is placed successfuly")
        else:
            messages.warning(
                request, "You cart is empty! Order is not placed with empty cart"
            )
        return redirect("myorders")


class MyOrdersView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, "userdash/myorders.html", {"orders": orders})


class OrderDetailView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            cartitems = CartItem.objects.filter(
                user=request.user, order=order
            ).annotate(stprice=F("quantity") * F("item__price"))
            total_items = sum(item.quantity for item in cartitems)
            total_price = sum(item.stprice for item in cartitems)
            return render(
                request,
                "userdash/myorder_details.html",
                {
                    "order": order,
                    "cartitems": cartitems,
                    "total_items": total_items,
                    "total_price": total_price,
                },
            )
        except:
            messages.warning(request, "You do not have this order")
            return redirect("myorders")


def changeQuantity(request, item_id, flag):
    if request.user.is_authenticated and not request.user.is_staff:
        try:
            cartitem = CartItem.objects.get(pk=item_id)
            item = Item.objects.get(pk=cartitem.item_id)
            cartitem = CartItem.objects.get(item=item, order=None, user=request.user)
            if flag == 1:
                cartitem.quantity += 1
                messages.success(request, "Quantity Increase by 1")
            else:
                if cartitem.quantity < 2:
                    cartitem.quantity = 1
                    messages.warning(request, "Cannot Decrease Quantity")
                else:
                    cartitem.quantity -= 1
                    messages.success(request, "Quantity Decrease by 1")
            cartitem.stprice = cartitem.quantity * item.price
            cartitem.save()

        except:
            messages.warning(request, "Item not exists for this operation")
    else:
        cart = request.session.get("cart", [])
        for cart_item in cart:
            if cart_item["id"] == item_id:
                if flag == 1:
                    cart_item["quantity"] += 1
                    messages.success(request, "Quantity Increase by 1")
                else:
                    if cart_item["quantity"] < 2:
                        cart_item["quantity"] = 1
                        messages.warning(request, "Cannot Decrease Quantity")
                    else:
                        cart_item["quantity"] -= 1
                        messages.success(request, "Quantity Decrease by 1")
                cart_item["stprice"] = cart_item["quantity"] * cart_item["price"]
                request.session.save()
        request.session["cart"] = cart
        request.session.save()


class IncrementQuantityView(View):
    def get(self, request, item_id):
        changeQuantity(request=request, item_id=item_id, flag=1)
        return redirect("mycart")


class DecrementQuantityView(View):
    def get(self, request, item_id):
        changeQuantity(request=request, item_id=item_id, flag=0)
        return redirect("mycart")
