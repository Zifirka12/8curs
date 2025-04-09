from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView

from rest_framework.permissions import IsAuthenticated
from materials.paginators import CustomPaginator
from materials.models import Lesson, Course, Subscription
from materials.serializer import LessonSerializer,LessonDetailSerializer,CourseSerializer

from users.permissions import IsModer, IsOwner
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.tasks import check_course_update
from django.shortcuts import get_object_or_404


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPaginator
    serializer_class = CourseSerializer

    def perform_update(self, serializer):
        """Обновление курса и асинхронная проверка изменений."""
        serializer.save()
        check_course_update.delay(self.kwargs["pk"])

    def get_permissions(self):
        """
        Определение разрешений в зависимости от действия.
        Создавать могут все аутентифицированные пользователи.
        Обновлять и удалять могут только модераторы или владельцы.
        """
        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создание нового урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer, IsAuthenticated)


class LessonListApiView(ListAPIView):
    """Список всех уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator


class LessonRetrieveApiView(RetrieveAPIView):
    """Получение подробной информации об уроке."""
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class LessonUpdateApiView(UpdateAPIView):
    """Редактирование существующего урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class LessonDestroyApiView(DestroyAPIView):
    """Удаление урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class SubView(APIView):
    """
    Подписка или отписка от курса.
    POST-запрос обрабатывается в зависимости от наличия подписки.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, pk=request.data.get("course_id"))

        subscription = Subscription.objects.filter(
            user=user,
            course=course
        ).first()

        if subscription:
            subscription.delete()
            message = "Подписка удалена."
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена."

        return Response({"message": message})
