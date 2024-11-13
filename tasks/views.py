from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .permissions import TaskCreatorPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from rest_framework.response import Response
from rest_framework import status


class TaskCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions, TaskCreatorPermission)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title']
    ordering_fields = ['due_date', 'title']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        if not queryset:
            return Response({
                "message": "Nenhuma tarefa encontrada."
            }, status=status.HTTP_404_NOT_FOUND)        
        return Response(serializer.data)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoModelPermissions, TaskCreatorPermission)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Tarefa deletada com sucesso."
        }, status=status.HTTP_204_NO_CONTENT)
