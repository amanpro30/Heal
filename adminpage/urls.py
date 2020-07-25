from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from .views import *
from django.contrib.auth import views as auth_views
app_name="adminpage"

urlpatterns = [
    
    url('',include('users.urls')),
    url('^admin1/adminpage/$',adminpage,name='adminpage'),
    url('^admin1/add_new_test',add_new_test,name='new_test')

      
    # path('adminpage/',adminpage, name='adminpage'),
    

]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
