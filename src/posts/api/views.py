from django.db.models import Q

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView
    ) 

from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny
    )

from ..models import Post
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer,
    PostCreateUpdateSerializer
    )
from .pagination import PostPagePagination
from .permissions import UserOwnerPermission

class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'content', 'user__first_name', 'user__last_name')
    ordering_fields = ('title', 'content')
    pagination_class = PostPagePagination
    permission_classes = (AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
        return queryset_list

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (AllowAny,)

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = (UserOwnerPermission, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = (UserOwnerPermission, IsAdminUser)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (UserOwnerPermission, IsAdminUser)

