
from rest_framework import viewsets, generics, filters, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, User
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

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]


