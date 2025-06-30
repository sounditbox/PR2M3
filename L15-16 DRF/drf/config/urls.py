from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('posts.urls', namespace='posts')),
    path('users/', include('users.urls', namespace='users')),
    path('api/v1/', include('posts.api.urls', namespace='api')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
