from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('longdozenapp.urls')),
    path('api/', include('longdozenapp.api.urls'))
]
