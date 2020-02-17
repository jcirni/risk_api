from django.test import TestCase

from ..records.models import Restaurant, Inspection, Violation, InspectionViolation


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

        cls.sample_inspection = Inspection.objects.create(
            inspection_date='2019-12-20',
            score=10,
            comments='sample inspection',
            restaurant_id=824,
            inspection_id=306
        )

        cls.sample_violation = Violation.objects.create(
            code='5',
            description='this is a health code violation',
            comments='comment',
            inspection_id=306,
            violation_id=8
        )

        cls.sample_inspection_violation = InspectionViolation.objects.create(
            violation_id=8,
            inspection_id=306,
        )


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
