from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('register',views.register,name='register'),
    path('login',views.Login,name='login'),
    path('history',views.history,name='history'),
    path('about_us',views.about_us,name='about_us'),
    path('contact_us',views.contact,name='contact_us'),
    path('profile',views.profile,name='profile'),
    path('edit_profile/<int:user_id>/',views.edit_profile,name='edit_profile'),
    path('edit_payment/<int:user_id>/',views.edit_payment_info,name='edit_payment_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
