from django.urls import path
from .views import dashboard_home, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', dashboard_home, name='dashboard-home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
