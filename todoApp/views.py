from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Todo, User
from .serializers import TodoSerializer
from rest_framework import status

# Create your views here.
class Todos(APIView):

  def get_user(self, user_id):
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      raise NotFound("유저를 찾을 수 없습니다.")
    return user
  
  def get(self, request, user_id):
    # month와 day 쿼리 파리미터로 받아서 필터링
    now = timezone.localtime(timezone.now())
    current_month = now.month
    current_day = now.day

    #쿼리 파라미터에 "month"값이 없으면, 디폴트 값으로 current_month 가져옴
    month = request.query_params.get("month", current_month)
    month = int(month)

    day = request.query_params.get("day", current_day)
    day = int(day)

    user = self.get_user(user_id)

    #Todo 객체를 월, 일 사용자로 필터링하여 가져옴
    todos = Todo.objects.filter(
      date__month=month,
      date__day=day,
      user=user
    )
    serializer = TodoSerializer(
      todos,
      many=True
    )
    return Response(serializer.data)
  
  def post(self, request, user_id):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
      user = self.get_user(user_id)
      serializer.save(
        user = user
      )
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
    
class TodoDetail(APIView):
  def get_user(self, user_id):
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      raise NotFound("유저를 찾을 수 없습니다.")
    return user
    
  def delete(self, request, user_id, todo_id):
    user = self.get_user(user_id)
    try: 
      todo = Todo.objects.get(user=user, id=todo_id)
    except Todo.DoesNotExist:
      raise NotFound("투두를 찾을 수 없습니다.")
    todo.delete()
    return Response({"message": "투두가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
  
  def patch(self, request, user_id, todo_id):
    user = self.get_user(user_id)
    try:
      todo = Todo.objects.get(user=user, id=todo_id)
    except Todo.DoesNotExist:
      raise NotFound("투두를 찾을 수 없습니다.")
    serializer = TodoSerializer(todo, data=request.data, partial=True) #partial=True는 부분업데이트 지원!
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  # 모델에 없는 필드를 request body에 넣어서 줘도 정상적으로 수정 가능????

# 클래스는 언제 나누는지