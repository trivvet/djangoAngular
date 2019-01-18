from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError
from django.urls import reverse

from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
    )

from accounts.api.serializers import AccountDetailSerializer
from ..models import Comment

User = get_user_model()

try:
    user_for_comment = User.objects.all().first()
except OperationalError:
    user_for_comment = None

class CommentCreateSerializer(ModelSerializer):
    model_type = serializers.CharField(write_only=True)
    slug = serializers.SlugField(write_only=True)
    parent_id = serializers.IntegerField(required=False)
    # user = user_for_comment

    class Meta:
        model = Comment
        fields = (
            'user',
            'id',
            'content',
            'model_type',
            'slug',
            'parent_id',
            'timestamp'
            )

    def validate(self, data):
        model_type = data.get("model_type", "post")
        model_qs = ContentType.objects.filter(model=model_type)
        if not model_qs.exists() or model_qs.count() != 1:
            raise ValidationError("This is not a valid content type")
        SomeModel = model_qs.first().model_class()
        slug = data.get("slug")
        obj_qs = SomeModel.objects.filter(slug=slug)
        if not obj_qs.exists() or obj_qs.count() != 1:
            raise ValidationError("This slug is not valid for this content type")
        parent_id = data.get("parent_id")
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if not parent_qs.exists() or parent_qs.count() != 1:
                raise ValidationError(
                    "This is not valid parent for this content")
        return data

    def create(self, validated_data):
        content = validated_data.get("content")
        main_user = self.context['user']
        model_type = validated_data.get("model_type", "post")
        slug = validated_data.get("slug")
        parent_id = validated_data.get("parent_id")
        parent_obj = None
        if parent_id:
            parent_obj = Comment.objects.filter(id=parent_id).first()
        comment = Comment.objects.create_by_model_type(
            model_type=model_type, slug=slug, content=content,
            user=main_user, parent_obj=parent_obj)
        return comment 

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
