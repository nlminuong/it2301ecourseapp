from rest_framework.serializers import ModelSerializer
from yaml import TagToken

from courses.models import Category, Course, Lesson, Tag, User, Comment
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # request = self.context.get('request'):
        if instance.image:
            data['image'] = instance.image.url

        return data


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject','image','category']


class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image','course']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

class LessonDetailsSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content','tags']

    def to_representation(self, lesson):
        data = super().to_representation(lesson)
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            data['like'] = lesson.like_set.filter(user=request.user, active=True).exists()

        return data

class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields =  ['id','first_name','last_name','email']

class UserSerializer(SimpleUserSerializer):
    class Meta:
        model = SimpleUserSerializer.Meta.model
        fields = SimpleUserSerializer.Meta.fields + ['username','password','avatar' ]
        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }
    def create(self, validated_data):
        user = User(**validated_data)

        user.set_password(user.password)
        user.save()

        return user



# Tạo CommentSerializer
# Qua ViewSet: tạo UserViewSet  ( có ảnh)

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user','lesson']
        extra_kwargs = {
            'lesson':{
                'write_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data