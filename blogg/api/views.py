from rest_framework import viewsets
from blogg.blogposts.models import Post, UserProfile, Follow, Like
from .serializers import PostSerializer, UserSerializer
from rest_framework import viewsets, permissions
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.models import Token
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

class CurrentUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user) 
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
            # Add more user fields as needed
        })


# get posts that loggedin users follows and its own posts
class DashboardView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def list(self, request):
        user = request.user
        following_ids = Follow.objects.filter(follower=user).values_list('followed_id', flat=True)
        queryset = Post.objects.filter(author__in=following_ids) | Post.objects.filter(author=user)
        queryset = queryset.annotate(num_likes=Count('like'))
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# userviewset with userprofile model

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Generate or retrieve the token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Login successful','token': token.key})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'message': 'Registration successful'})