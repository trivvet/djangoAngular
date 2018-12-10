from django.contrib.auth import (
    get_user_model
    )

from rest_framework.authentication import (
    SessionAuthentication, 
    BasicAuthentication
    )
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView
    ) 
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny
    )

from .serializers import (
    AccountListSerializer,
    AccountDetailSerializer,
    AccountCreateSerializer,
    AccountLoginSerializer
    )
User = get_user_model()

class AccountListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountListSerializer
    permission_classes = (IsAdminUser)

class AccountDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AccountDetailSerializer

class AccountCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountCreateSerializer
    permission_classes = (AllowAny)

class AccountLoginAPIView(APIView):
    serializer_class = AccountLoginSerializer

    # def get(self, request, format=None):
    #     # token = Token.objects.create(user=request.user)
    #     content = {
    #         'user': unicode(request.user),  # `django.contrib.auth.User` instance.
    #         'auth': unicode(request.auth),  # None
    #         # 'token': unicode(token)
    #     }
    #     return Response(content)

    def post(self, request, *args, **kwargs):
        data = request.POST
        serializer = self.serializer_class(data=data)
        # import pdb;pdb.set_trace()
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            # user = serializer.validated_data['username']
            # token, created = Token.objects.get(user=user)
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)