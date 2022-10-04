from django.urls import path

from .views import test_model_list_view, TestModelDetailView

urlpatterns = [
    path('', test_model_list_view),
    path('<int:pk>', TestModelDetailView.as_view(), name='test-detail'),
]