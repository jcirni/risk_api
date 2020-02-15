from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from ...utils.test_utils import BaseModelTestCase
from ...records.models import Restaurant

class RestaurantTestCase(BaseModelTestCase):


    def test_string_representation(self):
        r = Restaurant.objects.get(pk=1)
        self.assertEqual(str(r),r.name)

    def test_address_invalid_fails(self):
        r = Restaurant.objects.get(pk=1)
        r.street_address = 'this! is invalid'
        self.assertRaises(ValidationError, r.clean_fields)

    def test_duplicate_restaurant_fails(self):
        r = Restaurant.objects.get(pk=1)
        r.pk = None
        self.assertRaises(ValidationError, r.validate_unique)

    def test_invalid_state_fails(self):
        r = Restaurant.objects.get(pk=1)
        r.state = 'RR'
        self.assertRaises(ValidationError, r.clean_fields)
        
