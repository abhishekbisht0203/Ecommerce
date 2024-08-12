from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('product/', views.product, name="product"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('cart/', views.cart, name="cart"),
    path('payment/', views.payment, name="payment"),
    path('product_detail/', views.product_detail, name="product_detail"),
    path('form/', views.form, name="form"),
    path("addtocart/<int:product_id>/", views.addtocart, name="addtocart"),
    path("removefromcart/<int:product_id>/", views.removefromcart, name="removefromcart"),
    path('decreasequantity/<int:product_id>/', views.decrease_quantity, name="decreasequantity"),
]

