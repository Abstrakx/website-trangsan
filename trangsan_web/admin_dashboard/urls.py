from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import CustomLoginView, AduanViewSet,  UserViewSet, PeminjamanBarangViewSet, BarangViewSet, dashboard_aduan, update_status_aduan, dashboard_barang, delete_barang, edit_barang, dashboard_user, delete_user, edit_user, dashboard_peminjaman_barang, update_status_peminjaman, update_status_dikembalikan ,delete_peminjaman_barang

router = DefaultRouter()
router.register(r'aduan', AduanViewSet)
router.register(r'user', UserViewSet)
router.register(r'peminjaman', PeminjamanBarangViewSet)
router.register(r'barang', BarangViewSet)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
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
    path('update_status_dikembalikan/<str:peminjaman_id>/', update_status_dikembalikan, name='update_status_dikembalikan'),
    path('delete_peminjaman_barang/', delete_peminjaman_barang, name='delete_peminjaman_barang'),
]