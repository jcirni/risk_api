from django.db import models

from ..utils import records_validators as validators
from ..utils.model_utils import BaseModel


class Restaurant(BaseModel):
    restaurant_id = models.IntegerField(unique=True)
    name = models.TextField()
    street_address = models.TextField()
    city = models.TextField()
    state = models.CharField(max_length=2)
    # assume 5 digit area code, not +4zip
    postal_code = models.CharField(
        max_length=5, blank=True)
    # flag for updating aggregates only on new inspection data
    is_current = models.BooleanField(default=True)
    # value of -1 indidcates avg score has not been calculated yet
    sum_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    # value of -1 indidcates avg violations has not been calculated
    sum_violations = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    total_inspections = models.IntegerField(default=0)

    def average_score(self):
        if self.total_inspections == 0:
            return self.total_inspections
        return self.sum_score / self.total_inspections

    def average_violations(self):
        if self.sum_violations == 0:
            return self.total_inspections
        return self.sum_violations / self.total_inspections

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'street_address'], name='unique_restaurant')
        ]

    def __str__(self):
        return self.name

    def update_state(self):
        self.is_current = not self.is_current

    def update_total_score(self, value):
        """For singular inspection entry."""
        self.sum_score += value

    def update_total_violations(self, value):
        """For singular inspection entry."""
        self.sum_violations += value

    def update_total_inspections(self):
        """For singular ispection entry."""
        self.total_inspections += 1

    def update_aggregates(self, num_violations, score):
        """Maintains running aggregate values for single inspection entry"""
        self.update_total_inspections()
        self.update_total_violations(num_violations)
        self.update_total_score(score)
        self.is_current = True
        self.save()

    def calculate_avg_score(self, queryset):
        total = 0
        for entry in queryset:
            total += entry.score
        self.sum_score = total

    def calculate_avg_violations(self, queryset):
        self.sum_violations = queryset.count()

    def calculate_total_inspections(self, queryset):
        self.total_inspections = queryset.count()

    def calculate_aggregates(self):
        """ calculates all aggregates from scratch """
        inspections = self.inspections.all()
        self.calculate_total_inspections(inspections)
        self.calculate_avg_score(inspections)
        self.calculate_avg_violations(InspectionViolation.objects.filter(
            inspection__restaurant_id=self.restaurant_id))
        self.save()


class Inspection(BaseModel):
    inspection_id = models.IntegerField(
        unique=True, validators=[validators.valid_id])
    inspection_date = models.DateField(validators=[validators.valid_date])
    score = models.IntegerField(validators=[validators.valid_score])
    comments = models.TextField(blank=True)
    restaurant = models.ForeignKey(
        Restaurant,
        to_field='restaurant_id',
        on_delete=models.CASCADE,
        related_name='inspections'
    )

    def __str__(self):
        return f'{self.restaurant.name}, {self.score}'


class Violation(BaseModel):
    violation_id = models.IntegerField(
        unique=True, validators=[validators.valid_id])
    is_critical = models.BooleanField(default=False)
    code = models.CharField(max_length=24)
    description = models.TextField()
    comments = models.TextField(blank=True)
    is_repeat = models.BooleanField(default=False)
    is_corrected_on_site = models.BooleanField(default=False)
    inspection = models.ForeignKey(
        Inspection,
        to_field='inspection_id',
        on_delete=models.CASCADE,
        related_name='violations'
    )

    def __str__(self):
        return self.description


class InspectionViolation(models.Model):
    """Intermediate model for Inspection, and Violation"""
    violation = models.ForeignKey(
        Violation,
        to_field='violation_id',
        on_delete=models.CASCADE,
        null=True
    )
    inspection = models.ForeignKey(
        Inspection,
        to_field='inspection_id',
        on_delete=models.CASCADE,

    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['violation_id', 'inspection_id'],
                name='unique_inspection_violation')
        ]

    def __str__(self):
        return f'{self.violation_id}, {self.inspection_id}'
