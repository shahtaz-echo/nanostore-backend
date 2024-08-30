from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def index(request):
    return HttpResponse('App is running...')

urlpatterns = [
    path('', index ),
    path('admin/', admin.site.urls),
    path('api/', include('store.urls') )
]
