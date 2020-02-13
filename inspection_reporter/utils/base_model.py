from django.db import models

class BaseModel(models.Model):
    """abstracting common model behavior of id naming"""
    def __init__(self, *args, **kwargs):
        self.id = models.AutoField(primary_key=True, db_column=f'{self.__class__.__name__}_id'.lower())

    class Meta:
        abstract = True

    def __str__(self):
        return self.id