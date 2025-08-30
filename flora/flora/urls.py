"""
URL configuration for flora project.


"""
from django.contrib import admin
from django.urls import path,include
from flora import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   
    path('admin/', admin.site.urls),
  
    path('',views.home,name='home'),
    path('product_detail/<slug>/',views.product_detail,name='product_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/',views.cart,name='cart'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('order/<slug:slug>',views.order,name='order'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
   ]
 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)