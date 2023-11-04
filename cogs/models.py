from tortoise import fields
from tortoise.models import Model


class Employee(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=30, unique=True, index=True)


class Review(Model):
    employee_id = fields.UUIDField()
    rating = fields.FloatField()
    description = fields.TextField()
