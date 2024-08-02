from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.TaskCreateListView.as_view(), name='task-create-list-view'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyView.as_view(), name='task-detail-view'),
]