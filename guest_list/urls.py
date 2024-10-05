from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/all-guests', views.all_guests, name='all_guests'),
    path('dashboard/notified-guests', views.notified_guests, name='notified_guests'),
    path('dashboard/not-notified-guests', views.not_notified_guests, name='not_notified_guests'),
    path('send-qr-to-one/', views.send_qr_to_one, name='send_qr_to_one'),
    path('import-guest-list/', views.import_guest_list, name='import_guest_list'),
    path('send-qr-to-all/', views.send_qr_to_all, name='send_qr_to_all'),
    path('export-notified-to-excel/', views.export_notified_to_excel, name='export_notified_to_excel'),
    path('export-not-notified-to-excel/', views.export_not_notified_to_excel, name='export_not_notified_to_excel'),
    path('export-to-excel/', views.export_to_excel, name='export_to_excel'),
    # path('scan-qr-code/', views.scan_qr_code, name='scan_qr_code'),
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
