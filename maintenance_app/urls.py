from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'maintenance_app'


urlpatterns = [
    # Tenant URLs
    path('submit_request/', views.submit_maintenance_request, name='submit_maintenance_request'),

    # Staff URLs
    path('view_requests/', views.view_requests, name='view_requests'),
    path('update_request/<int:request_id>/', views.update_request_status, name='update_request_status'),

    # Manager URLs
    path('add_tenant/', views.add_tenant, name='add_tenant'),
    path('move_tenant/<int:tenant_id>/', views.move_tenant, name='move_tenant'),
    path('delete_tenant/<int:tenant_id>/', views.delete_tenant, name='delete_tenant'),


    path('tenant_view/', views.tenant_view, name='tenant_view'),
    path('manager_view/', views.manager_view, name='manager_view'),
    path('maintenance_view/', views.maintenance_view, name='maintenance_view'),
    path('', views.homepage, name='homepage'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)