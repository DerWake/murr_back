from django.contrib.auth import get_user_model
import uuid
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from murren.models import SignUpTokens
from murren.serializers import MurrenSerializers, PublicMurrenInfoSerializers

Murren = get_user_model()


class MurrensMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        r = Murren.objects.get(id=request.user.id)
        data = {'murren_name': r.username}
        return Response(data)


class GetTanochkaImg(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {'img_url': '/media/tanochka.jpg'}
        return Response(data)


class PublicMurrenInfo(APIView):

    def get(self, request, pk):
        r = Murren.objects.get(id=pk)
        serializer = PublicMurrenInfoSerializers(r, context={'request': request})
        return Response(serializer.data)


class GetAllMurrens(ListAPIView):
    queryset = Murren.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = MurrenSerializers
    pagination_class = PageNumberPagination


class TokenCheck(APIView):

    def post(self, request):
        return Response(request)


class TokenGenerate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            token = str(uuid.uuid4())[:6]
            SignUpTokens.objects.create(uuid=token, owner=request.user)
            return Response(token)
        return Response('Ты не суперюзер! =)')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
