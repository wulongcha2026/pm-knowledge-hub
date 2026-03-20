from django.urls import path
from . import views

app_name = 'rag'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
]
