from rest_framework import serializers
from blogg.blogposts.models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content','author_id' , 'author_username', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.like_set.count()


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.ReadOnlyField(source='userprofile.bio')
    profile_picture = serializers.ReadOnlyField(source='userprofile.profile_picture.url')
    class Meta:
        model = User
        fields = ['id', 'username','bio', 'profile_picture']


