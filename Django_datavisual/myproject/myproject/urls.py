"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#這邊可以管理所有的url
#可以在此連接到view
from django.contrib import admin
from django.urls import path

from catalog import views

from django.conf.urls import include
from django.contrib import admin



from django.contrib import admin
from django.urls import path
from .import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/',  views.showCart , name = "showCart") ,
    path('', views.login),
    path('login/', views.login),
    path('logout/', views.logout),	
    path("register/",views.addtest),
    path("userOrder/",views.searchUserOrder , name="userOrder" ),
    path("cart/add/<pk>",views.addCart ,name ="addcart" ),
    path('captcha/', include('captcha.urls')),
    path("login1/",views.resultProduct, name="food_list"),
    path("login1/<str:productType>",views.resultProduct ),
    path("login12/",views.BooksListView.as_view(), name="BooksListView"),
    path("login123/<pk>",views.foodDetailview, name="foodDetailview"),
    path("/cart/delete_cart/<pk>" ,views.removeCart, name="removeCart"),
    path("place/" ,views.place_order, name="placeOrder"),
    path("submit_order/" ,views.submit_order, name="submitOrder"),
    path("submit_order/submit_success/<pk>" ,views.submit_success, name="SubmitSuccess"),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
    
    
