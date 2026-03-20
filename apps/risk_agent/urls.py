from django.urls import path
from . import views

app_name = 'risk_agent'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('api/analyze/', views.analyze_api, name='analyze_api'),
    path('<int:pk>/', views.detail, name='detail'),
]
