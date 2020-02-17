from django.db import models

from ..utils import records_validators as validators
from ..utils.model_utils import BaseModel


class Restaurant(BaseModel):
    restaurant_id = models.IntegerField(unique=True)
    name = models.TextField()
    street_address = models.TextField(validators=[validators.valid_address])
    city = models.TextField()
    state = models.CharField(max_length=2, validators=[
                             validators.valid_state_abbrev])
    # assume 5 digit area code, not +4zip
    postal_code = models.CharField(
        max_length=5, blank=True, validators=[validators.valid_zip])
    # flag for updating aggregates only on new inspection data
    is_current = models.BooleanField(default=True)
    average_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=-1.00)
    average_violations = models.DecimalField(
        max_digits=5, decimal_places=2, default=-1.00)
    total_inspection = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'street_address'], name='unique_restaurant')
        ]

    def __str__(self):
        return self.name


class Inspection(BaseModel):
    inspection_id = models.IntegerField(unique=True)
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
    violation_id = models.IntegerField(unique=True)
    is_critical = models.BooleanField(default=False)
    code = models.CharField(max_length=24)
    description = models.TextField()
    comments = models.TextField(blank=True)
    # TODO:Verify against code if not provided
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
