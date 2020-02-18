from django.core.exceptions import ValidationError

from ...utils.test_utils import BaseModelTestCase
from ...records.models import Restaurant, InspectionViolation
from ...risk_api.serializers import InspectionSerializer


class RestaurantTestCase(BaseModelTestCase):

    def test_string_representation(self):
        r = Restaurant.objects.get(pk=1)
        self.assertEqual(str(r), r.name)

    def test_same_name_and_address_fails(self):
        r = Restaurant.objects.get(pk=1)
        r.pk = None
        self.assertRaises(ValidationError, r.validate_unique)

    def test_calculate_total_inspection_correct(self):
        r = Restaurant.objects.get(pk=1)
        r.calculate_aggregates()
        self.assertEqual(r.total_inspections, r.inspections.all().count())

    def test_calculate_avg_violations_correct(self):
        r = Restaurant.objects.get(pk=1)
        r.calculate_aggregates()
        violations = InspectionViolation.objects.filter(
            inspection__restaurant_id=r.restaurant_id).count()
        inspections = r.inspections.all().count()
        calculated_average = violations/inspections
        self.assertEqual(r.average_violations(),
                         calculated_average, msg=InspectionViolation.objects.filter(
            inspection__restaurant_id=r.restaurant_id))

    def test_calculate_avg_score_correct(self):
        r = Restaurant.objects.get(pk=1)
        r.calculate_aggregates()
        inspections = r.inspections.all()
        sum_score = 0
        for restaurant in inspections:
            sum_score += restaurant.score
        calculated_average = sum_score / inspections.count()
        self.assertEqual(r.average_score(), calculated_average)

    def test_update_average_score_correct(self):
        r = Restaurant.objects.get(pk=1)
        inspections = r.inspections.all()
        sum_score = 0
        for restaurant in inspections:
            sum_score += restaurant.score
        calculated_average = sum_score / inspections.count()
        self.assertEqual(r.average_score(),
                         calculated_average)

    def test_update_average_violation_correct(self):
        r = Restaurant.objects.get(pk=1)
        violations = InspectionViolation.objects.filter(
            inspection__restaurant_id=r.restaurant_id).count()
        inspections = r.inspections.all().count()
        calculated_average = violations / inspections
        self.assertEqual(r.average_violations(), calculated_average)

    def test_update_total_inspections_correct(self):
        r = Restaurant.objects.get(pk=1)
        inspections = r.inspections.all().count()

        # make copy and alter sample inpsection data
        i_copy = dict(self.inspection_data)
        for violation in i_copy['violations']:
            violation['violation_id'] = violation['violation_id'] + 100
        i_copy['inspection_id'] = 999
        serializer = InspectionSerializer(data=i_copy)
        if not serializer.is_valid():
            self.fail(serializer.errors)
        serializer.create(serializer.validated_data)
        r = Restaurant.objects.get(pk=1)
        self.assertEqual(r.total_inspections, inspections + 1)
