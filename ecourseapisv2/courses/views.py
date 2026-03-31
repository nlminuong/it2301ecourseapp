from asyncio import create_subprocess_exec

from rest_framework import viewsets, generics, filters, status, parsers, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

import perms
from courses.models import Category, Course, Lesson, User, Comment, Like
from courses import serializers
from courses.paginators import ItemPaginator


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = ItemPaginator
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject']
    ordering_fields = ['id']

    def get_queryset(self):
        query = self.queryset

        q = self.request.query_params.get('q')

        if q:
            query = query.filter(subject__icontains=q)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            query = query.filter(category_id=category_id)


        return query

    @action(methods=['GET'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        course = self.get_object()
        lessons = course.lesson_set.filter(active=True)

        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)

class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_permissions(self):
        if self.action in ['get_comment', 'like'] and self.request.method.__eq__('POST'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny]
    @action(methods=['GET','POST'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            s = serializers.CommentSerializer(data = {
                'content': request.data.get('content'),
                'user': request.user.pk,
                'lesson': self.get_object().pk
            })
            s.is_valid(raise_exception=True)
            c = s.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_200_OK)
        comments = self.get_object().comment_set.select_related('user').filter(active=True)
        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='like',detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object() )
        if not created:
            like.active = not like.active
        like.save()
        return Response(
            self.serializer_class(self.get_object(), context={'request': request}).data,
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser] #dùng để xử lý dữ liệu gửi lên dạng form-data (multipart)

    @action(methods=['GET','PATCH'], detail=False, url_path='current-user', permission_classes = [permissions.IsAuthenticated])
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PATCH'):
            s = serializers.SimpleUserSerializer(u, data={
                'first_name' : request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'email': request.data.get('email'),

            })
            s.is_valid(raise_exception=True)
            u = s.save()
        return Response(serializers.UserSerializer(u).data, status = status.HTTP_200_OK)



class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]




