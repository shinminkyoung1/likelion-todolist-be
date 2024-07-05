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
    
    def get(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get(self, request, user_id):
        # 현재 날짜 및 시간 가져오기
        now = timezone.localtime(timezone.now())
        current_month = now.month
        current_day = now.day

        # 쿼리 파라미터에서 month와 day 값 가져오기, 없으면 디폴트 값으로 현재 month와 day 사용
        month = request.query_params.get("month", current_month)
        month = int(month)

        day = request.query_params.get("day", current_day)
        day = int(day)

        # 유저 가져오기
        user = self.get_user(user_id)

        # 기본 필터링: month와 day에 맞는 투두 항목들 가져오기
        todos = Todo.objects.filter(
            date__month=month,
            date__day=day,
            user=user
        )

        # 정렬 및 추가 필터링을 위한 sort_by 파라미터 가져오기
        sort_by = request.query_params.get('sort_by', 'created_at')
        if sort_by not in ['created_at', 'updated_at', 'is_bookmarked']:
            sort_by = 'created_at'

        # 북마크 필터링 적용
        if sort_by == 'is_bookmarked':
            todos = todos.filter(is_bookmarked=True).order_by('-created_at')
        else:
            todos = todos.order_by(f'-{sort_by}')

        # 직렬화
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    
    def post(self, request, user_id):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_user(user_id)
            serializer.save(
                user=user
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def get_todo(self, user, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("투두 항목을 찾을 수 없습니다.")
        return todo
    
    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch_bookmark(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        data = {'is_bookmarked': request.data.get('is_bookmarked')}
        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch_dark_mode(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        data = {'dark_mode': request.data.get('dark_mode')}
        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoCheck(APIView):

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get_todo(self, user, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("투두 항목을 찾을 수 없습니다.")
        return todo

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        data = {'is_checked': request.data.get('is_checked')}
        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TodoReview(APIView):

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get_todo(self, user, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("투두 항목을 찾을 수 없습니다.")
        return todo

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        data = {'emoji': request.data.get('emoji')}
        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

