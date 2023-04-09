from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only='True', required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('__all__')


class TitleModifySerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug')
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('__all__')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, attrs):
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id'))
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    title_id=title, author_id=author).exists():
                raise serializers.ValidationError(
                    'You have already left a review for this title!')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def validate(self, attrs):
        get_object_or_404(
            Review,
            title_id=self.context['view'].kwargs.get('title_id'),
            id=self.context['view'].kwargs.get('review_id')
        )
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """ Serializer to process other users profile management API requests.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(
                'Username \'me\' is reserved, please choose another one'
            )
        if User.objects.filter(
            username__iexact=value
        ).exists():
            raise ValidationError(
                'A user with that username already exists.'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(
            email__iexact=value
        ).exists():
            raise ValidationError(
                'user with this Email address already exists.'
            )
        return value


class UserRoleReadOnlySerializer(UserSerializer):
    """ Serializer to process own user profile management API requests.
    Role field change is restricted.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ['role']


class AuthSignupSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthTokenSerializer(serializers.Serializer):

    username = serializers.RegexField(r'^[\w.@+-]+$', max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('confirmation_code')
        user = get_object_or_404(User, username=attrs.get('username'))
        if not default_token_generator.check_token(user, token):
            raise ValidationError('Invalid token')
        return attrs
