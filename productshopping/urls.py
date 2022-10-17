from django.conf.urls.static import static
from django.urls import path

from goshopee import settings
from productshopping import views

urlpatterns = [
    path('', views.showhome,name='home'),
    path('artwork-product-details/<int:pid>', views.showproductdetails, name='productdetails'),
    # path('artwork-size-details/<int:pid>', views.showproductsizedetails, name='productdetails'),
    path('add-to-shopping-cart',views.addtoshoppingcart, name='addshoppingcart'),
    path('show-cart',views.showshoppingcart, name='shoppingcart'),
    path('delete-product-from-cart/<int:id>',views.deleteproductfromcart, name='deletefromcart'),
    path('Wishlist',views.addtowishlist, name='addtowishlist'),
    path('Show-Wishlist',views.showwishlist, name='showwishlist'),
    path('delete-product-from-wishlist/<int:id>',views.deleteproductfromwishlist, name='deletefromwish'),
    path('signup',views.MySignUpClass.as_view(), name='signup'),
    path('sign-in', views.showlogin, name='signin'),
    path('signout', views.mylogout, name='signout'),
    path('checkout',views.mycheckout,name='checkout'),
    path('order-success',views.showordersuccess,name='ordersuccess'),
    path('final-order',views.finalorder,name='finalorder'),
    path('product-categories/<int:cid>',views.productcategories,name='productcategories'),
    path('order-history',views.orderhistory,name='orderhistory'),
    path('order-details/<int:oid>',views.orderdetails,name='orderdetails'),
    path('update-profile/<int:pk>',views.updateprofile.as_view(),name='updateprofile'),
    path('profile', views.add_user, name='profile'),
    path('change-password',views.changepswd,name='changepass')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)