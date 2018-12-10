from django.db.models import Q

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
    ) 
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny
    )

from ..models import Comment
from .pagination import CommentPagePagination
from .serializers import (
    CommentListSerializer, 
    CommentDetailSerializer,
    CommentChildSerializer,
    create_comment_serializer
    )

class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentListSerializer
    permission_classes = (AllowAny,)
    pagination_class = CommentPagePagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (
        'user__username',
        'content'
    )

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(user__username__icontains=query)|
                Q(content__icontains=query)
                ).distinct()
        return queryset_list

# class CommentChildListAPIView(ListAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentChildSerializer
#     permission_classes = (IsAuthenticated, IsAdminUser)
#     lookup_field = 'parent'

class CommentDetailAPIView(RetrieveAPIView, UpdateModelMixin, DestroyModelMixin):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = (AllowAny)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(
            type=model_type, 
            slug=slug, 
            parent_id=parent_id,
            user = self.request.user
            )