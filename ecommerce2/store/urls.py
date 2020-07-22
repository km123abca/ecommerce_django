from django.urls import path
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
]