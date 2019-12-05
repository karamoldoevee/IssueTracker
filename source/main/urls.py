from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/v2/', include('api_v2.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)