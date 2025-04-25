from base.models import User,Post
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
     
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_datetime', 'username']

    def get_username(self, obj):
        return obj.user.name

    def to_internal_value(self, data):

        isPost = self.context.get('request').method == 'POST'
        if isPost:
            self._username = data.get('username')
            if not self._username:
                raise serializers.ValidationError({'username': 'This field is required.'})
            return super().to_internal_value(data)
        else:
            return super().to_internal_value(data)

    def create(self, validated_data):
        user, created =  User.objects.get_or_create(name=self._username) 
        return Post.objects.create(user=user, **validated_data)
    def get_view_name(self):
        return "Posts API"