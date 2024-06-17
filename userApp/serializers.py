from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from .models import User

class UserSerializer(ModelSerializer):

  class Meta:
    model = User
    fields = "__all__"