from rest_framework import serializers
from rest_framework.templatetags.rest_framework import data

from main.models import Post, CodeImage, Reply, Comment, Like, Rating


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image', )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Post
        fields = ('id', 'title', 'discription', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['images'] = ImageSerializer(instance.images.all(), many=True).data
        representation['likes'] = instance.likes.count()
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
        return representation



    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        print(request.user )
        post = Post.objects.create( author=request.user, **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, post=post)

        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance,key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(
                image=image,
                post=instance
            )
        return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Reply
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(
                instance.comments.all(), many=True
            ).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment


class RatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__' #('star', 'post')

    def create(self, validated_data):
        request = self.context.get('request')
        email = request.user
        post = validated_data.get('product')

        if Rating.objects.filter(author=email, post=post):
            rating = Rating.objects.get(author=email, post=post)
            return rating

        rating = Rating.objects.create(author=request.user, **validated_data)
        return rating





class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post')

        if Like.objects.filter(user=user, post=post):
            like = Like.objects.get(user=user, post=post)
            return like

        like = Like.objects.create(user=user, **validated_data)
        return like
