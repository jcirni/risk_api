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
        cls.inspection_data = {
            "inspection_id": 34078,
            "inspection_date": "2018-06-02",
            "score": 88,
            "comments": "Discussed employee illness policy with PIC. Discussed clean up procedures with PIC.",
            "violations": [{
                "violation_id": 1004,
                "is_critical": True,
                "code": "5",
                "description": "Hands clean and properly washed",
                "comments": "Observed BOH employee handle raw chicken, rinse hands w/ water only, then handle non-food-contact surfaces and money. Corrected on site with notice to PIC."
            },
            {
                "violation_id": 1005,
                "is_critical": True,
                "code": "6",
                "description": "Proper hot holding temperatures",
                "comments": "Chicken @145f, beef @138f"
            }, {
                "violation_id": 1006,
                "is_critical": False,
                "code": "27",
                "description": "Gloves used properly",
                "comments": ""
            }, {
                "violation_id": 1007,
                "is_critical": True,
                "code": "8",
                "description": "Toxic substances properly identified, stored, and used",
                "comments": "Sanitizer stored above produce (COS)"
            }],
            "restaurant": {
                "restaurant_id": 201,
                "name": "SKINNER'S DINNERS",
                "street_address": "3325-A SKINNER HOLLOW RD",
                "city": "HAINES",
                "state": "OR",
                "postal_code": "97833"
            }
        }


    def setUp(self):
        self.client = APIClient()

    def test_post_valid_json_passes(self):
        self.client.post('/inspection',self.inspection_data, format='json')
        #expected entries # of violations, #of inspectionviolations and restaurant
        expected_entries = len(self.inspection_data['violations']) * 2 + 1
        serializer = InspectionSerializer(data=self.inspection_data)
        if not serializer.is_valid():
            self.fail(serializer.errors)
        #collection of target tables
        entries = [
            Violation.objects.all(), 
            InspectionViolation.objects.all(), 
            Restaurant.objects.all()
        ]
        #get initial count of related tables
        baseline = 0
        for entry in entries:
            baseline += entry.count()
        #update tables
        serializer.create(serializer.validated_data)
        #get new count of updated table
        new_count = 0
        for entry in entries:
            new_count += entry.count()
        new_count = new_count - baseline
        self.assertEqual(expected_entries, new_count, f'expected: {expected_entries} counted: {new_count}')
 
    def test_retrieve_inspection_correct_record(self):
        self.client.post('/api/inspection/',self.inspection_data, format='json')
        path = f"/api/inspection/{self.inspection_data['inspection_id']}/"
        i = self.client.get(path, format='json')

        if i.status_code == 200:
            self.assertEqual(self.inspection_data['inspection_id'], i.data['inspection_id'])
        else:
            self.fail(f'Failed to retrieve object with {i.status_code} at {request}') 
        

    def test_create_inspection_same_restaurant_passes(self):
        """New Inspection of same restaurant does not try to create a new restaurant entry.
        
        serializer = InspectionSerializer(data=self.inspection_data)
        if not serializer.is_valid():
            self.fail(serializer.errors)
        #create initial inspection and restaurant
        serializer.create(serializer.validated_data)
        #modify inspection ID to add new entry with same restaurant
        serializer = InspectionSerializer(data=self.inspection_data)
        serializer.initial_data['inspection_id'] = 303
        serializer.is_valid()
        rs = Restaurant.objects.all()
        old_count = rs.count()
        serializer.create(serializer.validated_data)
        new_count = rs.count()
        #There should be no difference
        self.assertEquals(old_count, new_count)

        """
   



        
