from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

from .serializers import InspectionSerializer
from inspection_reporter.records.models import Inspection

#TODO: Retrieve Restaurant inspection history

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

    def retrieve(self, request, pk=None):
        inspection = get_object_or_404(self.queryset, inspection_id=pk)
        serializer = self.serializer_class(inspection)
        return Response(serializer.data)

