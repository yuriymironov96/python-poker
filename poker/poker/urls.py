from django.urls import path

from . import views


urlpatterns = [
    path('hands', views.HandListCreateApiView.as_view(), name='hands_view'),
]