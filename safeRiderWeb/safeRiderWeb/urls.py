from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-site/', include('base2.urls')),
    path('', include('base.urls')),
    path('apis/', include('apis.urls')),
    path('fare-pay/<pk>/', views.mpesa_callback)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
