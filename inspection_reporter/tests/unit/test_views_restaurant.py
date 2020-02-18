from django.test import TestCase

from rest_framework.test import APIClient


class RestaurantViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.inspection_data = {
            "inspection_id": 34078,
            "inspection_date": "2018-06-02",
            "score": 88,
            "comments": ("Discussed employee illness policy with PIC. "
                         "Discussedclean up procedures with PIC."),
            "violations": [{
                "violation_id": 1004,
                "is_critical": True,
                "code": "5",
                "description": "Hands clean and properly washed",
                "comments": ("Observed BOH employee handle raw chicken, rinse "
                             "hands w/ water only, then handle non-food-"
                             "contact surfaces and money. Corrected on site "
                             "with notice to PIC.")
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
                "description": ("Toxic substances properly identified, stored,"
                                " and used"),
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
        self.restaurant_data = {
            "restaurant_id": 1251,
            "name": "S DINNERS",
            "street_address": "3325-A SKINNER HOLLOW RD",
            "city": "HAINES",
            "state": "OR",
            "postal_code": "97833"
        }

    def test_post_valid_json_passes(self):
        r = self.client.post('/api/restaurant/',
                             self.restaurant_data, format='json')
        self.assertEqual(r.status_code, 200, msg=r.status_code)

    def test_post_invalid_id_fails_400(self):
        self.restaurant_data['restaurant_id'] = -1
        r = self.client.post('/api/restaurant/',
                             self.restaurant_data, format='json')
        self.assertEqual(r.status_code, 400, msg=r.status_code)

    def test_post_invalid_street_fails_400(self):
        self.restaurant_data['street_address'] = 'Th!s St'
        r = self.client.post('/api/restaurant/',
                             self.restaurant_data, format='json')
        self.assertEqual(r.status_code, 400, msg=r.status_code)

    def test_invalid_state_fails_400(self):
        self.restaurant_data['state'] = 'RR'
        r = self.client.post('/api/restaurant/',
                             self.restaurant_data, format='json')
        self.assertEqual(r.status_code, 400, msg=r.status_code)

    def test_invalid_zip_code_fails_400(self):
        self.restaurant_data['postal_code'] = 'forty'
        r = self.client.post('/api/restaurant/',
                             self.restaurant_data, format='json')
        self.assertEqual(r.status_code, 400, msg=r.status_code)

    def test_retrieve_restaurant_correct_record(self):
        self.client.post('/api/restaurant/',
                         self.restaurant_data, format='json')
        path = f"/api/restaurant/{self.restaurant_data['restaurant_id']}/"
        i = self.client.get(path, format='json')

        if i.status_code == 200:
            self.assertEqual(
                self.restaurant_data['restaurant_id'], i.data['restaurant_id'])
        else:
            self.fail(
                f'Failed to retrieve object with {i.status_code}.',
                f'Tried using {self.restaurant_data}')