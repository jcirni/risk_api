from django.db import models
from inspection_reporter.utils import records_validators as validators
from inspection_reporter.utils.base_model import BaseModel

class Restaurant(BaseModel):
    name = models.TextField()
    street_address = models.TextField(validators=[validators.is_valid_address])
    city = models.TextField()
    state = models.CharField(max_length=2,validators=[validators.is_valid_state_abbrev])
    postal_code = models.CharField(max_length=5,validators=[validators.is_valid_zip])
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Violation(BaseModel):
    is_critical = models.BooleanField()
    code = models.TextField()
    description = models.TextField()
    comments = models.TextField(default='', blank=True)

    def __str__(self):
        return self.code

class Inspection(BaseModel):
    date = models.DateField()
    score = models.IntegerField()
    comments = models.TextField()
    restaurant_id = models.ForeignKey(
                        Restaurant, 
                        on_delete=models.CASCADE
                    )

class RestaurantInspectionViolations(models.Model):
    restaurant_id = models.ForeignKey(
                        Restaurant,
                        on_delete=models.CASCADE,
                    )
    violation_id = models.ForeignKey(
                        Violation,
                        on_delete=models.CASCADE
                    )
    inspection_id = models.ForeignKey(
                        Inspection,
                        on_delete=models.CASCADE
                    )
    average_score = models.DecimalField(max_digits=5, decimal_places=2)
    average_violations = models.DecimalField(max_digits=5,decimal_places=2)
    



    