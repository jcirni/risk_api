from inspection_reporter.utils.test_utils import BaseSerializerTestCase

from django.core.exceptions import ValidationError

from inspection_reporter.records.models import Restaurant, Inspection, Violation, InspectionViolation

from inspection_reporter.risk_api.serializers import InspectionSerializer


class InspectionSerializerTestCase(BaseSerializerTestCase):
    
    def test_create_related_entries_exist(self):
        """InspectionSerializer.create() should add a Restaurant, Violations, and InspectionViolations.
        
        Fail Condition:  # of entries expected in do no match # of entries out
        """
        #Inspection will add entries to Violations, InspectionViolation and restaurant
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

    def test_create_inspection_same_restaurant_passes(self):
        """New Inspection of same restaurant does not try to create a new restaurant entry."""
        data = self.inspection_data
        serializer = InspectionSerializer(data=data)
        if not serializer.is_valid():
            self.fail(serializer.errors)
        #create initial inspection and restaurant
        serializer.create(serializer.validated_data)
        #modify inspection ID to add new entry with same restaurant
        data = self.inspection_data
        data['inspection_id'] = 302
        for violation in data['violations']:
            violation['violation_id'] = violation['violation_id'] + 100
        serializer = InspectionSerializer(data=data)
        if not serializer.is_valid():
            self.fail(serializer.errors)
        
        rs = Restaurant.objects.all()
        old_count = rs.count()
        serializer.create(serializer.validated_data)
        new_count = rs.count()
        #There should be no difference
        self.assertEquals(old_count, new_count)

        
   



        
