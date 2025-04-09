from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
from django.utils import timezone
from users.models import Payment, User
from users.serializer import PaymentsSerializers, UserSerializer
from users.services import create_price, create_stripe_product, create_stripe_session


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializers
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['paid_course', 'separately_paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']

    def perform_create(self, serializer):
         payment = serializer.save(user=self.request.user, date = timezone.now().date())
         product = create_stripe_product(payment)
         price = create_price(payment.payment_summ, product)
         session_id, payment_link = create_stripe_session(price)
         payment.session_id = session_id
         payment.link = payment_link
         payment.save()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()