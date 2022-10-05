from django.urls import path

from .views import index, TestModelDetailView

urlpatterns = [
    path('', index),
    path('<int:pk>', TestModelDetailView.as_view(), name='test-detail'),
]