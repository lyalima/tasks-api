from rest_framework import serializers
from .models import Task
from datetime import date


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'creator', 'description', 
                  'due_date', 'created_at', 'updated_at')


    def validate_due_date(self, value):
        current_date = date.today()
        if value < current_date:
            raise serializers.ValidationError(
                'A data de vencimento não pode ser anterior à data atual.')
        return value
