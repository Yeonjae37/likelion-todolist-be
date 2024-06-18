from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import User

# Create your views here.
class Register(APIView):
    
  def post(self, request):
    #1. 사용자 요청으로 데이터 받음
    #2. 그 데이터로 Serializer 객체 만듬
    serializer = UserSerializer(data=request.data)
    #3. 그 데이터 유효하면
    if serializer.is_valid():
    #4. 저장
      serializer.save()
      return Response({
        "detail": "회원가입 요청이 성공적으로 처리되었습니다."
      })
    else:
      return Response(serializer.errors)
    
class Login(APIView):
  # 유저를 가져오는 함수(우리가 정의)
  def get_user(self, username, password):
    try:
      user = User.objects.get(username=username, password=password)
      return user
    except User.DoesNotExist:
      raise NotFound("유저를 찾을 수 없습니다.")
    
  # 로그인
  def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
      raise ParseError("username 또는 password가 필요합니다.")
    user = self.get_user(username, password)
    return Response({
      # 유저 식별 시 사용될 user의 ID 응답해주기
      "user_id": user.id
    })