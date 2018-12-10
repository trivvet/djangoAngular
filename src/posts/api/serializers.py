from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
    )

from comments.models import Comment
from comments.api.serializers import CommentSerializer
from accounts.api.serializers import AccountDetailSerializer

from ..models import Post

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:post_detail',
        lookup_field='pk')
    edit_url = HyperlinkedIdentityField(
        view_name="posts-api:post_update",
        lookup_field='pk')
    user = AccountDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'url', 
            'edit_url',
            'user', 
            'title', 
            'content', 
            'image', 
            'slug', 
            'publish'
        )

class PostDetailSerializer(ModelSerializer):
    user = AccountDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = (
            'title', 
            'content', 
            'user', 
            'image', 
            'publish',
            'html',
            'comments'
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None

    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        return CommentSerializer(obj.comments, many=True).data

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'publish')


    # title = serializers.CharField(max_length=200)
    # content = serializers.CharField()
    # image = serializers.ImageField()
    # draft = serializers.BooleanField()
    # publish = serializers.DateField()