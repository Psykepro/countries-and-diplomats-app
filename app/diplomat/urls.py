from django.urls import path

from .views import (DiplomatListView, DiplomatUpdateView, DiplomatDelete,
                    DiplomatDetailView, DiplomatCreateView)

urlpatterns = [
    path('', DiplomatListView.as_view(), name='diplomat-list'),
    path('<int:pk>/edit', DiplomatUpdateView.as_view(), name='diplomat-edit'),
    path('<int:pk>/delete', DiplomatDelete.as_view(), name='diplomat-delete'),
    path('<int:pk>', DiplomatDetailView.as_view(), name='diplomat-detail'),
    path('new', DiplomatCreateView.as_view(), name='diplomat-new'),
]
