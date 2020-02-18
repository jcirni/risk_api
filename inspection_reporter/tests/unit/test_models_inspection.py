from django.core.exceptions import ValidationError

from ...records.models import Inspection
from ...utils.test_utils import BaseModelTestCase


from datetime import datetime, timedelta


class InspectionModelTestCase(BaseModelTestCase):

    def test_string_representation(self):
        i = Inspection.objects.get(pk=1)
        self.assertEqual(str(i), f'{i.restaurant.name}, {i.score}')

    def test_future_date_fails(self):
        i = Inspection.objects.get(pk=1)
        i.inspection_date = datetime.date(datetime.now()) + timedelta(days=1)
        self.assertRaises(ValidationError, i.clean_fields)

    def test_invalid_score_fails(self):
        i = Inspection.objects.get(pk=1)
        i.score = 101
        self.assertRaises(ValidationError, i.clean_fields)

    def test_negative_score_fails(self):
        i = Inspection.objects.get(pk=1)
        i.score = -1
        self.assertRaises(ValidationError, i.clean_fields)
