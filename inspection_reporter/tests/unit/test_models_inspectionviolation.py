from django.db.utils import IntegrityError

from ...utils.test_utils import BaseModelTestCase
from ...records.models import InspectionViolation

from datetime import datetime,timedelta

class InspectionViolationModelTestCase(BaseModelTestCase):
    
    def setUp(self):
        self.iv = InspectionViolation.objects.get(pk=1)
    
    def test_string_representation(self):
        self.assertEqual(str(self.iv), f'{self.iv.violation_id}, {self.iv.inspection_id}')

    def test_duplicate_fails(self):
        self.iv.pk = None
        self.assertRaises(IntegrityError, self.iv.save)



        
