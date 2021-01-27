from rest_framework import serializers

from api.models import User, Post, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'username', 'password')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.save()

        return user


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('title', 'content', 'created_by',)


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    post_id = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = ('user_id', 'post_id', 'creation_date',)


class PostLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('user_id',)

    def update(self, instance, validated_data):
        user_id = validated_data['user_id']
        user = User.objects.filter(id=user_id).first()
        if user in instance.likes.all():
            instance.likes.remove(user)
        else:
            like = Like(user=user, post=instance)
            like.save()
        instance.save()
        return instance
