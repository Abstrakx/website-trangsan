from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import CustomLoginView, AduanViewSet,  UserViewSet, PeminjamanBarangViewSet, BarangViewSet, dashboard_aduan, update_status_aduan, dashboard_barang, delete_barang, edit_barang, dashboard_user, delete_user, edit_user, dashboard_peminjaman_barang, update_status_peminjaman, update_status_dikembalikan, delete_peminjaman_barang, detect_qr_code, user_detail, update_status_absensi, user_login, user_logout, homepage_login, homepage_main, homepage_peminjaman, homepage_peminjaman_user, update_status_dikembalikan_user, homepage_aduan, user_aduan_form, homepage_pegawai

router = DefaultRouter()
router.register(r'aduan', AduanViewSet)
router.register(r'user', UserViewSet)
router.register(r'peminjaman', PeminjamanBarangViewSet)
router.register(r'barang', BarangViewSet)

urlpatterns = [
    # Admin dashboard URLS
    path('login/', CustomLoginView.as_view(), name='login'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
    path('api/detect_qr_code/', detect_qr_code, name='detect_qr_code'),
    path('dashboard_aduan/', dashboard_aduan, name='dashboard_aduan'),
    path('update_status_aduan/<int:aduan_id>/', update_status_aduan, name='update_status_aduan'),
    path('dashboard_barang/', dashboard_barang, name='dashboard_barang'),
    path('delete_barang/', delete_barang, name='delete_barang'),
    path('edit_barang/', edit_barang, name='edit_barang'),
    path('dashboard_user/', dashboard_user, name='dashboard_user'),
    path('delete_user/', delete_user, name='delete_user'),
    path('edit_user/', edit_user, name='edit_user'),
    path('dashboard_peminjaman_barang/', dashboard_peminjaman_barang, name='dashboard_peminjaman_barang'),
    path('update_status_peminjaman/<str:peminjaman_id>/', update_status_peminjaman, name='update_status_peminjaman'),
    path('update_status_dikembalikan/', update_status_dikembalikan, name='update_status_dikembalikan'),
    path('delete_peminjaman_barang/', delete_peminjaman_barang, name='delete_peminjaman_barang'),
    path('user_detail/<str:id_user>/', user_detail, name='user_detail'),
    path('update-status-absensi/<str:id_user>/<int:index>/', update_status_absensi, name='update_status_absensi'),

    # User URLS
    path('', homepage_login, name='homepage_login'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('home/<str:id_user>/', homepage_main, name='homepage_main'),
    path('home/peminjaman/<str:id_user>/', homepage_peminjaman, name='homepage_peminjaman'),
    path('home/peminjaman_user/<str:id_user>/', homepage_peminjaman_user, name='homepage_peminjaman_user'),
    path('home/peminjaman_user/<str:id_user>/update_status_dikembalikan/', update_status_dikembalikan_user, name='update_status_dikembalikan_user'),
    path('home/aduan/<str:id_user>/', homepage_aduan, name='homepage_aduan'),
    path('home/aduan/<str:id_user>/form/', user_aduan_form, name='user_aduan_form'),
    path('home/pegawai/<str:id_user>', homepage_pegawai, name='homepage_pegawai'),
]