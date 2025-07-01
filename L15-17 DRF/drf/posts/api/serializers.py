from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField

from posts.models import Comment, Category, Tag, Article


class CommentSerializer(serializers.ModelSerializer):
    article = StringRelatedField(read_only=True)
    article_id = PrimaryKeyRelatedField(queryset=Article.objects.all())
    author = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class ArticleSerializer(serializers.ModelSerializer):
    # author = StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['views', 'created_at', 'updated_at',
                            'id', 'author', 'status']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Article.objects.all(),
                fields=['title', 'content']
            )
        ]

    def validate_title(self, value):
        if 'test' in value.lower():
            raise serializers.ValidationError('Title cannot contain "test"')
        return value

    def validate(self, attrs):
        if 'spam' in attrs['content'].lower():
            raise serializers.ValidationError('Content cannot contain "spam"')
        return attrs

    def create(self, validated_data):
        category = validated_data.pop('category')
        tags = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        article.category = Category.objects.get_or_create(**category)[0]
        article.save()
        article.tags.set(tags)

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = AuthorSerializer(instance.author).data
        return representation
