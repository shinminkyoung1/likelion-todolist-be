from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__" # user 클래스에 있는 모든 필드들을 userserializer에서 사용하겠다!