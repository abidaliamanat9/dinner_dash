import factory
from authentication.models import User
from dashboard.models.cartitem_model import CartItem, Order
from dashboard.models.item_model import Item, Category
from dashboard.models.resturant_model import Resturant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = f"{first_name}.{last_name}@gmail.com"
    password = factory.PostGenerationMethodCall("set_password", "test1234")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class ResturantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resturant

    name = factory.Sequence(lambda n: f"Resturant {n}")


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    title = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("paragraph")
    price = factory.Faker("random_number", digits=2)
    retired = False
    resturant = factory.SubFactory(ResturantFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    order = factory.SubFactory(OrderFactory)
    quantity = factory.Faker("random_number", digits=2)
    price = factory.Faker("random_number", digits=2)
    item = factory.SubFactory(ItemFactory)
    user = factory.SubFactory(UserFactory)
