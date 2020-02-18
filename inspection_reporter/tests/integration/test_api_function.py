from django.test import TestCase

from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework.test import APIClient

from ...records.models import Restaurant, Inspection, Violation, InspectionViolation
from ...risk_api.serializers import InspectionSerializer

import json


class InspectionViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.inspection_data = {}

    def setUp(self):
        self.client = APIClient()

    def test_post_valid_json_passes(self):
        self.client.post('/inspection', self.inspection_data, format='json')
