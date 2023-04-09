from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from api.permissions import IsAdmin, IsAuthor, IsModerator, IsUser, ReadOnly
from api.serializers import (
    AuthSignupSerializer, AuthTokenSerializer,
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleGetSerializer, TitleModifySerializer,
    UserSerializer, UserRoleReadOnlySerializer,
)
from .filters import TitleFilter


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = [IsAdmin | IsAdminUser]

    @action(
        ["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=UserRoleReadOnlySerializer
    )
    def me(self, request):
        """ Function to process API requests with users/me/ URI.
        """
        self.kwargs['username'] = request.user
        if request.method == "GET":
            return self.retrieve(request)
        elif request.method == "PATCH":
            return self.partial_update(request)


class AuthViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSignupSerializer
    permission_classes = [AllowAny]

    def send_confirmation_code(self, user):
        """Function to generate token and send it to user via registered email.
        """
        confirmation_code = default_token_generator.make_token(user)
        email_text = (
            f'To confirm user {user} registration '
            f'please use {confirmation_code} code.'
        )
        user.email_user(
            settings.REGISTRATION_EMAIL_SUBJECT,
            email_text,
            settings.REGISTRATION_EMAIL_FROM,
            fail_silently=False,
        )

    @action(["post"], detail=False)
    def signup(self, request):
        """ Function to process API requests with auth/signup/ URI.
        """
        try:
            user = User.objects.get(
                username__iexact=request.data.get('username'),
                email__iexact=request.data.get('email')
            )
        except ObjectDoesNotExist:
            serializer = AuthSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                self.send_confirmation_code(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        self.send_confirmation_code(user)
        return Response(request.data, status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def token(self, request):
        """Function to process API requests with auth/token/
        """
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username'))
            tokens = RefreshToken.for_user(user)
            return Response(
                data={'token': str(tokens.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(ModelViewSet):
    queryset = (Title.
                objects.
                prefetch_related('genre').
                select_related('category').
                annotate(rating=Avg('reviews__score')).
                order_by('id')
                )
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    action_serializers = {
        'list': TitleGetSerializer,
        'retrieve': TitleGetSerializer,
        'create': TitleModifySerializer,
        'update': TitleModifySerializer,
        'partial_update': TitleModifySerializer,
        'destroy': TitleModifySerializer
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action)


class ListCreateDestroyViewSet(GenericViewSet,
                               ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin):
    """
        General class for views with only
        List, Create and Destroy functionality
    """
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Genre.objects.all().order_by('id')


class CategoryViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Category.objects.all().order_by('id')


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsUser & IsAuthor | IsModerator | IsAdmin | ReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id).order_by('pub_date')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsUser & IsAuthor | IsModerator | IsAdmin | ReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id).order_by('pub_date')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)
