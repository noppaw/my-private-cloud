from django.urls import path
from .views import MicroAppListView

urlpatterns = [
    path('apps/', MicroAppListView.as_view(), name='microapp-list'),
]