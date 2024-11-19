from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Alert
from .serializers import AlertSerializer


class AlertResource(APIView):
    """
    API for managing alerts.
    """

    def get(self, request, alert_id=None):
        """
        Retrieve a single alert by ID or all alerts.
        """
        if alert_id:
            alert = get_object_or_404(Alert, id=alert_id)
            serializer = AlertSerializer(alert)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            alerts = Alert.objects.all()
            serializer = AlertSerializer(alerts, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new alert.
        """
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            alert = serializer.save()
            return Response({'message': 'Alert created successfully', 'data': AlertSerializer(alert).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, alert_id):
        """
        Update an existing alert.
        """
        alert = get_object_or_404(Alert, id=alert_id)
        serializer = AlertSerializer(alert, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            updated_alert = serializer.save()
            return Response({'message': 'Alert updated successfully', 'data': AlertSerializer(updated_alert).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, alert_id):
        """
        Delete an alert by ID.
        """
        alert = get_object_or_404(Alert, id=alert_id)
        alert.delete()
        return Response({'message': 'Alert deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
