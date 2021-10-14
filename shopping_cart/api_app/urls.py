from django.urls import path
from .views import ShoppingCart, ShoppingCartUpdate, ShowCommit

urlpatterns = [
    path('cart-items/', ShoppingCart.as_view()),
    path('update-item/<int:item_id>', ShoppingCartUpdate.as_view()),
    path('show/', ShowCommit.as_view()),
]
