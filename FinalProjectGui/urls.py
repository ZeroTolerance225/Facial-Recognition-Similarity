from django.contrib import admin
from django.urls import path, include
from maintenance_app import views as maintenance_views  # Import views from maintenance_app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maintenance/', include('maintenance_app.urls')),
    path('', maintenance_views.homepage, name='homepage'),  # Corrected to use the view from maintenance_app
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)