from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import CustomLoginView, AduanViewSet, dashboard_aduan, update_status_aduan, dashboard_barang, delete_barang, edit_barang, dashboard_user, delete_user, edit_user

router = DefaultRouter()
router.register(r'aduan', AduanViewSet)

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
]