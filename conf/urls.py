from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from shop.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('shop.urls')),
    path('api/v1/', include(router.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
