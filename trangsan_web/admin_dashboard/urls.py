from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import CustomLoginView ,AduanViewSet, dashboard_aduan, update_status_aduan

router = DefaultRouter()
router.register(r'aduan', AduanViewSet)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
    path('dashboard_aduan/', dashboard_aduan, name='dashboard_aduan'),
    path('update_status_aduan/<int:aduan_id>/', update_status_aduan, name='update_status_aduan'),
]