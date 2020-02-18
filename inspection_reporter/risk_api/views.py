from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets, status

from .serializers import (InspectionSerializer,
                          RestaurantSerializer, HistorySerializer)
from ..records.models import Inspection, Restaurant


class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

    def retrieve(self, request, pk=None):
        inspection = get_object_or_404(self.queryset, inspection_id=pk)
        serializer = self.serializer_class(inspection)
        return Response(serializer.data)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            r = serializer.create(serializer.validated_data)
            r.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        restaurant = get_object_or_404(self.queryset, restaurant_id=pk)
        restaurant_data = HistorySerializer(restaurant)
        return Response(restaurant_data.data)
