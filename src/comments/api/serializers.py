from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
    )

from accounts.api.serializers import AccountDetailSerializer
from ..models import Comment

User = get_user_model()

def create_comment_serializer(type='post', 
    slug=None, parent_id=None, user=User.objects.all().first()):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = (
                'user',
                'content',
                'timestamp'
                )

        def __init__ (self, *args, **kwargs):
            self.model_type = type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parend_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()

            return super(CommentCreateSerializer, self).__init__(
                *args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This slug is not valid for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            main_user = user
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type=model_type, slug=slug, content=content,
                user=main_user, parent_obj=parent_obj)
            return comment 

    return CommentCreateSerializer

class CommentSerializer(ModelSerializer):
    # children_list_url = HyperlinkedIdentityField(
    #     view_name="comments-api:comments_child_list",
    #     lookup_field='id')
    reply_count = SerializerMethodField()
    # detail_url = HyperlinkedIdentityField(
    #     view_name="comments-api:comment_detail")

    class Meta:
        model = Comment
        fields = (
            'id',
            'content_type',
            'content',
            'parent',
            # 'children_list_url',
            # 'detail_url',
            'reply_count',
            'timestamp'
        )

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        else:
            return 0

class CommentListSerializer(ModelSerializer):
    # children_list_url = HyperlinkedIdentityField(
    #     view_name="comments-api:comments_child_list",
    #     lookup_field='id')
    reply_count = SerializerMethodField()
    url = HyperlinkedIdentityField(
         view_name="comments-api:comment_detail")

    class Meta:
        model = Comment
        fields = (
            'id',
            'url',
            # 'content_type',
            'content',
            # 'parent',
            # 'children_list_url',
            # 'detail_url',
            'reply_count',
            'timestamp'
        )

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        else:
            return 0

class CommentChildSerializer(ModelSerializer):
    user = AccountDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content',
            'timestamp',
            'parent'
        )

class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    user = AccountDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content_object_url',
            'object_id',
            'content',
            'replies',
            'reply_count',
            'timestamp'
        )
        read_only_fields = (
            'id',
            'user',
            'content_type',
            'object_id',
            'replies',
            'reply_count'
        )

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), 
                many=True).data

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        else:
            return 0

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None
