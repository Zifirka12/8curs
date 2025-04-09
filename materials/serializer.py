from materials.validators import YoutubeURLValidator
from materials.models import Course, Lesson, Subscription
from rest_framework import serializers


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        validators = [YoutubeURLValidator(field='video')]

    def get_lesson_count(self, instance):
        return instance.lessons.all().count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        new_course = Course.objects.create(**validated_data)
        for lesson in lessons:
            Lesson.objects.create(**lesson, course=new_course)
        return new_course


class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class LessonDetailSerializer:
    pass
