from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.select_related()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
