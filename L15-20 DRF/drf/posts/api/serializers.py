from django.contrib.auth import get_user_model
from rest_framework import serializers

from config import settings
from posts.models import Comment, Category, Tag, Article


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    text = serializers.CharField(source='content')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'article', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    comments = CommentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display',
                                           read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'image', 'author', 'category', 'tags',
            'comments', 'views', 'created_at', 'updated_at', 'status',
            'status_display'
        ]
        read_only_fields = [
            'id', 'author', 'views', 'created_at', 'updated_at',
            'comments', 'status_display'
        ]

    def validate_title(self, value):
        return value.strip()

    def validate_content(self, value):
        return value.strip()

    def validate_image(self, image):
        if image and image.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be under 2MB")
        return image

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['tags'] = TagSerializer(instance.tags.all(),
                                               many=True).data
        return representation


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)

    def validate(self, data):

        if not self.context['user'].check_password(data['old_password']):
            raise serializers.ValidationError("Old password is incorrect")

        if data['new_password'] != data['repeat_password']:
            raise serializers.ValidationError("Passwords do not match")

        return data
