from tortoise.models import Model
from tortoise import fields


class Employee(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=30, unique=True, index=True)
    average_rating = fields.FloatField(default=0.0)


class Review(Model):
    employee_id = fields.UUIDField()
    rating = fields.FloatField()
    description = fields.TextField()


def setup(_):
    pass
