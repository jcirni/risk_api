from django.test import TestCase

from ..records.models import Restaurant, Inspection, Violation, InspectionViolation
from ..risk_api.serializers import InspectionSerializer


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.mickyd_data = {
            'name': 'Micky\'s',
            'street_address': '630 Lenox Ave Unit J',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10037',
            'is_current': True,
            'restaurant_id': 824
        }
        cls.sample_restaurant = Restaurant.objects.create(**cls.mickyd_data)

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
                'name': 'Micky\'s',
                'street_address': '630 Lenox Ave Unit J',
                'city': 'New York',
                'state': 'NY',
                'postal_code': '10037',
                'is_current': True,
                'restaurant_id': 824
            }
        }
        serializer = InspectionSerializer(data=cls.inspection_data)
        serializer.is_valid()
        serializer.create(serializer.validated_data)

        cls.inspection_data2 = {
            "inspection_id": 34079,
            "inspection_date": "2018-06-02",
            "score": 88,
            "comments": "Discussed employee illness policy with PIC. Discussed clean up procedures with PIC.",
            "violations": [{
                "violation_id": 1014,
                "is_critical": True,
                "code": "5",
                "description": "Hands clean and properly washed",
                "comments": "Observed BOH employee handle raw chicken, rinse hands w/ water only, then handle non-food-contact surfaces and money. Corrected on site with notice to PIC."
            },
                {
                "violation_id": 1015,
                    "is_critical": True,
                    "code": "6",
                    "description": "Proper hot holding temperatures",
                    "comments": "Chicken @145f, beef @138f"
            }, {
                    "violation_id": 1016,
                    "is_critical": False,
                    "code": "27",
                    "description": "Gloves used properly",
                    "comments": ""
            }, {
                    "violation_id": 1017,
                    "is_critical": True,
                    "code": "8",
                    "description": "Toxic substances properly identified, stored, and used",
                    "comments": "Sanitizer stored above produce (COS)"
            }],
            "restaurant": {
                'name': 'Micky\'s',
                'street_address': '630 Lenox Ave Unit J',
                'city': 'New York',
                'state': 'NY',
                'postal_code': '10037',
                'is_current': True,
                'restaurant_id': 824
            }
        }
        serializer = InspectionSerializer(data=cls.inspection_data2)
        serializer.is_valid()
        serializer.create(serializer.validated_data)


class BaseSerializerTestCase(TestCase):

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
