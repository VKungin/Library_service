from rest_framework import generics
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    PaymentSuccessSerializer,
)


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        session_url = serializer.data.get("session_url")
        return Response({"url": session_url})


class PaymentSuccessView(generics.RetrieveAPIView):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentSuccessSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "paid"
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PaymentCancelView(generics.RetrieveAPIView):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "canceled"
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
