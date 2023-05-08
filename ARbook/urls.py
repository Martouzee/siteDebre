from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),

    # API route
    path('view-interne/<str:interne>', views.interne_view, name="interne"),
]