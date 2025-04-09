from rest_framework.serializers import ValidationError


class YoutubeURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in value and value is not None:
            raise ValidationError("Put only youtube videos' URLs")