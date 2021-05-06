from tortoise import fields
from tortoise.models import Model

from app.infra.postgres.models import Dog


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(unique=True, max_length=25)
    name = fields.CharField(max_length=20)
    password = fields.TextField()
    active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    registered_dogs: fields.ReverseRelation[Dog]
    adopted_dogs: fields.ReverseRelation[Dog]

    class Meta:
        table = "users"
