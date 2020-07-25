from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order')
    # url(r'^(?!.*(images/))',views.noSuchPage,name='noPage'),
]