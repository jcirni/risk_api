from ...utils.test_utils import BaseModelTestCase

from django.core.exceptions import ValidationError

from inspection_reporter.records.models import Inspection, Violation

from datetime import datetime,timedelta

class ViolationTestCase(BaseModelTestCase):
    

    def test_string_representation(self):
        v = Violation.objects.get(pk=1)
        self.assertEqual(str(v), v.description)




        
