from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/',include('lead.urls')),
    path('api/v1/',include('team.urls')),
    path('api/v1/',include('client.urls')),
    path('api/v1/',include('userprofile.urls')),
    path('api/v1/',include('emails.urls')),
    path('api/v1/',include('tasks.urls')),
    path('api/v1/',include('products.urls')),
    path('api/v1/',include('core.urls')),
    path('api/v1/',include('ai_assistant.urls')),
    path('silk/',include('silk.urls',namespace='silk')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT)
