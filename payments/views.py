from rest_framework import generics

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentSuccessView(generics.ListAPIView):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentSerializer


class PaymentCancelView(generics.RetrieveAPIView):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentSerializer
