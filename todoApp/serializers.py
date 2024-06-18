from rest_framework import serilaizers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField(read_only=True)
  #StringRelatedField : User 모델의 __str__ 메서드에 정의했던 String을 가져옴
  todo_id = serializers.IntegerField(source='id', read_only=True)

  class Meta:
    model = Todo
    fields = [
      'todo_id',
      'user',
      'date',
      'content',
      'is_checked',
      'emoji',
    ]